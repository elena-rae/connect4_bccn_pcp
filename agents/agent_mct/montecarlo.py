import numpy as np
import time
from agents.common import *
from agents.agent_minimax.minimax import get_valid_columns


def generate_move_montecarlo(
        board: np.ndarray, player: BoardPiece, saved_state: Optional[SavedState]
) -> Tuple[PlayerAction, Optional[SavedState]]:
    """
    generate move function employing monte carlo tree search algorithm
    Parameters
    -----------
    board: np.ndarray  # board reflecting current game state
    player: BoardPiece  # player for which the mcts algorithm is supposed to calculate an action
    saved_state: parameter for saving game tree -> not implemented
    Return
    -----------
    action  # presumably best action for player
    """
    action = mcts_algorithm(board, player)

    return action, saved_state


class Node:
    def __init__(self, board, player, move=None, parent=None, ):
        """Node of the game tree
        :type board: np.ndarray
        """
        self.wins = 0  # of wins for the node
        self.sims = 0  # of simulations of the node
        self.active_player = player  # active player of the current node
        self.opp_player = PLAYER2 if player == PLAYER1 else PLAYER1
        self.board = board.copy()  # current board state of that node
        self.move = move  # move from preceding board state, that led to this node
        self.parent = parent
        self.child_nodes = []
        self.possibleMoves = get_valid_columns(board)

    def mcts_selection(self):
        """
        Calculate UCB values of the child nodes of the node passed into the function
        Return:
        ------------------------
        selected_node: child with the highest UCB value """
        ucb_values = np.zeros(len(self.child_nodes))

        for i, child in enumerate(self.child_nodes):
            ucb_values[i] = child.calc_ucb(n_tot=self.sims)
        maximum = np.argmax(ucb_values)

        selected_node = self.child_nodes[maximum]

        return selected_node

    def calc_ucb(self, n_tot):
        """
        Upper Confidence Bound 1 - calculation
        Parameters
        -----------
        self.wins: # of wins for the node, considered after the i-th move
        self.sims: # of simulations of the node, considered after the i-th move
        n_tot: total number of simulations run by the parent node, after the i-th move
        c: exploration parameter
        Return:
        ----------------
        ucb: ucb value of the respective node
        """
        c = np.sqrt(2)
        ucb = self.wins / self.sims + c * (np.sqrt(np.log(n_tot) / self.sims))
        return ucb

    def mcts_expansion(self):
        """
        Expand game tree by randomly choosing one of the nodes possible moves, applying this action to the board
        Return:
        ------------------
        new_node: new child node, saved in the game tree
        """
        action = np.random.choice(self.possibleMoves)
        exp_board = apply_player_action(self.board, action, self.active_player, True)

        new_node = Node(exp_board, self.opp_player, action, self)
        self.possibleMoves.remove(action)
        self.child_nodes.append(new_node)

        return new_node

    def mcts_simulate(self):
        """
        play random moves for PLAYER1 and PLAYER2 alternating, until final GamesState(.IS_WIN or .IS_DRAW) is reached
        Parameters:
        ----------------
        board: board reflecting current game state after expansion
        player: active player of the expanded node
        Return:
        ----------------
        next_player: winner (PLAYER1 or PLAYER2) of the simulation
        GameState.IS_DRAW: -1 in case simulation ended with a draw
        """
        """ check if expanded node is an end state (i.e if last move finished the game)"""
        if check_end_state(self.board, self.opp_player) == GameState.IS_WIN:
            return self.opp_player  # player which won the game when expanding

        """ apply random actions until final GamesState(.IS_WIN or .IS_DRAW) is reached"""
        next_player = PLAYER1 if self.active_player == PLAYER2 else PLAYER2
        sim_board = self.board.copy()

        while check_end_state(sim_board, next_player) == GameState.STILL_PLAYING:
            next_player = PLAYER1 if next_player == PLAYER2 else PLAYER2
            valid_columns = get_valid_columns(sim_board)
            random_action = np.random.choice(valid_columns, size=1)
            sim_board = apply_player_action(sim_board, random_action, next_player)

        """evaluate the end state of the simulation and return the winnign player ( or -1 in case of draw)"""
        if check_end_state(sim_board, next_player) != GameState.IS_DRAW:
            return next_player  # winning player of the simulation either 1 or 2
        else:
            return GameState.IS_DRAW  # -1

    def pick_best_action(self):
        """
        Evaluate wins and simulations counter of the root node
        Return:
        ------------------------
        best_child: child with the highest value (child.wins / child.sims)"""
        child_values = np.zeros(len(self.child_nodes))
        for i, child in enumerate(self.child_nodes):
            child_values[i] = child.wins / child.sims

        maximum = np.argmax(child_values)
        best_child = self.child_nodes[maximum]

        return best_child


def mcts_algorithm(board: np.ndarray, player: BoardPiece, runtime=10):
    """
    Monte Carlo Tree Search algorithm with 4 steps: Selection, Expansion, Simulation, Backpropagation
    Parameters
    ----------------
    board: board reflecting current game state
    player:  player for which mcts algorithm is supposed to calculate an action
    runtime: max runtime for the agent
    Return
    ----------------
    best_child.move: move (action) corresponding to the presumably best action for the current game state
    """

    root_node = Node(board, player, move=None, parent=None)  # initialize root node with current board state
    counter = 0
    start_time = time.time()
    while (time.time() - start_time) < runtime:
        counter += 1
        node = root_node

        """MCTS SELECTION (according to UCB values)"""
        while node.child_nodes != [] and node.possibleMoves == []:
            node = node.mcts_selection()

        EXPANDED = False
        """MCTS EXPANSION """
        if node.possibleMoves:
            node = node.mcts_expansion()

            EXPANDED = True  # enables back propagation, only after successfully expanding

            winner = node.mcts_simulate()  # winning player (1 or 2) of simulation (or -1 in case of GameStage.IS_DRAW)

        """MCTS BACKPROPAGATION"""
        if EXPANDED:
            while node is not None:
                node.sims += 1
                if node.opp_player == winner:
                    node.wins += 1
                node = node.parent

    # ToDo: introduce exit condition for final game phase (i.e. if there are no more nodes to explore.) #

    """evaluate game tree and return action, corresponding to the most promising child_node"""
    best_child = root_node.pick_best_action()
    print(counter)
    return best_child.move

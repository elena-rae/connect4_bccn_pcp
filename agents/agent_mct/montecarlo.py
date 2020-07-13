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
    action = mcts_algorithm(board, player, runtime=5)

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
            ucb_values[i] = calc_ucb(child.wins, child.sims, self.sims)
        maximum = np.argmax(ucb_values)

        selected_node = self.child_nodes[maximum]

        return selected_node

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


def calc_ucb(wins: int, sims: int, n_tot: int, c=np.sqrt(2)) -> float:
    """
    Upper Confidence Bound 1 - calculation
    Parameters
    -----------
    wins: # of wins for the node, considered after the i-th move
    sims: # of simulations of the node, considered after the i-th move
    n_tot: total number of simulations run by the parent node, after the i-th move
    c: exploration parameter
    Return:
    ----------------
    ucb: ucb value of the respective node
    """

    ucb = wins / sims + c * (np.sqrt(np.log(n_tot) / sims))
    return ucb


def mcts_algorithm(board: np.ndarray, player: BoardPiece, runtime=5):
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

    start_time = time.time()
    while (time.time() - start_time) < runtime:
        node = root_node

        """MCTS SELECTION (according to UCB values)"""
        while node.child_nodes != [] and node.possibleMoves == []:
            node = node.mcts_selection()

        """MCTS EXPANSION """
        if node.possibleMoves:
            # if node.possibleMoves != []:

            node = node.mcts_expansion()

            win_count = 0

            """ check if expanded node is an end state (i.e if last move coincidentally finished the game)"""
            if check_end_state(node.board, node.opp_player) == GameState.IS_WIN:
                """ raise win counter if the end state is a win for the agent """
                if node.opp_player == root_node.active_player:
                    win_count = 1

            "start simulation if expanded node is a STILL_PLAYING board"""
            if check_end_state(node.board, node.opp_player) == GameState.STILL_PLAYING:

                """MCTS SIMULATION """
                winning_player = simulate_randomly(node.board.copy(), node.active_player)  # [1,2] or -1 if GameState.IS_DRAW
                if winning_player == root_node.active_player:
                    win_count = 1

        """MCTS BACKPROPAGATION"""
        while node.parent is not None:
            node.sims += 1
            node.wins += win_count
            node = node.parent

        node.sims += 1  # one last update for the root node
        node.wins += win_count

    # ToDo: introduce exit condition for final game phase (i.e. if there are no more nodes to explore.) #

    """evaluate game tree and return action, corresponding to the most promising child_node"""
    best_child = node.pick_best_action()

    return best_child.move


def simulate_randomly(board: np.ndarray, player: BoardPiece):
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

    next_player = PLAYER1 if player == PLAYER2 else PLAYER2

    while check_end_state(board, next_player) == GameState.STILL_PLAYING:
        next_player = PLAYER1 if next_player == PLAYER2 else PLAYER2
        valid_columns = get_valid_columns(board)
        random_action = np.random.choice(valid_columns, size=1)
        board = apply_player_action(board, random_action, next_player)

    if check_end_state(board, next_player) != GameState.IS_DRAW:
        return next_player  # either 1 or 2
    else:
        return GameState.IS_DRAW  # -1
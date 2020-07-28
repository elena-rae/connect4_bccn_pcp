from agents.agent_mct.montecarlo import *
from tests.test_common import *


def test_initialize_node():
    """test initialization of Node class"""
    
    board = initialize_game_state()
    node = Node(board, PLAYER1)
    valid_cols = get_valid_columns(board)
    assert node.wins == 0
    assert node.sims == 0
    assert node.active_player == PLAYER1
    assert node.opp_player == PLAYER2
    assert node.board.all() == board.all()
    assert node.move is None
    assert node.parent is None
    assert node.child_nodes == []
    assert node.possibleMoves == valid_cols


def test_mcts_expansion():
    """test expansion function of mcts algorithm"""

    board = initialize_game_state()
    node = Node(board, PLAYER1)
    new_node = node.mcts_expansion()

    assert new_node.parent == node
    assert node.child_nodes == [new_node]
    assert not np.any(node.possibleMoves == new_node.move)
    assert node.opp_player == new_node.active_player
    assert new_node.active_player == node.opp_player


def test_mcts_simulate():
    """test simulate function of mcts algorithm"""

    """test if correct value is returned when passed a draw board"""
    draw_board = generate_draw_board()
    node = Node(draw_board, PLAYER1)
    draw_winner = node.mcts_simulate()
    assert draw_winner == GameState.IS_DRAW

    """test if correct value (winner) is returned when passed a winning board"""
    win_board = np.array([[1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1],
                              [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
    node = Node(win_board, PLAYER1)
    winner = node.mcts_simulate()
    assert winner == PLAYER1


def test_mcts_immediate_win():
    """test mcts algorithm for immediate win cases for the agent"""

    """test if agent wins vertical 4-connect"""
    board_w_v = generate_win_board(VERTICAL, PLAYER1, apply_last_action=False)
    action = mcts_algorithm(board_w_v, PLAYER1)
    board_w_v = apply_player_action(board_w_v, action, PLAYER1)
    # print(pretty_print_board(board_w_v))
    assert check_end_state(board_w_v, PLAYER1) == GameState.IS_WIN

    """test if agent wins horizontal 4-connect"""
    board_w_h = generate_win_board(HORIZONTAL, PLAYER1, apply_last_action=False)
    action = mcts_algorithm(board_w_h, PLAYER1)
    board_w_h = apply_player_action(board_w_h, action, PLAYER1)
    # print(pretty_print_board(board_w_h))
    assert check_end_state(board_w_h, PLAYER1) == GameState.IS_WIN

    """test if agent wins diagonal 4-connect"""
    board_w_d = generate_win_board(DIAGONAL, PLAYER1, apply_last_action=False)
    action = mcts_algorithm(board_w_d, PLAYER1)
    board_w_d = apply_player_action(board_w_d, action, PLAYER1)
    # print(pretty_print_board(board_w_d))
    assert check_end_state(board_w_d, PLAYER1) == GameState.IS_WIN


def test_mcts_immediate_loose():
    """test if msct agent is able to preventing immediate opponent wins"""

    """test if agent prevents opponent from winning vertical 4-connect"""
    board_l_v = generate_win_board(VERTICAL, PLAYER2, apply_last_action=False, block_opponent_win=True)
    # print(pretty_print_board(board_l_v))
    action = mcts_algorithm(board_l_v, PLAYER1)
    board_l_v = apply_player_action(board_l_v, action, PLAYER1)
    board_l_v = apply_player_action(board_l_v, 5, PLAYER2)
    # print(pretty_print_board(board_l_v))
    assert not check_end_state(board_l_v, PLAYER2) == GameState.IS_WIN

    """test if agent prevents opponent from winning horizontal 4-connect"""
    board_l_h = generate_win_board(HORIZONTAL, PLAYER2, apply_last_action=False, block_opponent_win=True)
    # print(pretty_print_board(board_l_h))
    action = mcts_algorithm(board_l_h, PLAYER1)
    board_l_h = apply_player_action(board_l_h, action, PLAYER1)
    board_l_h = apply_player_action(board_l_h, 5, PLAYER2)
    # print(pretty_print_board(board_l_h))
    assert not check_end_state(board_l_h, PLAYER2) == GameState.IS_WIN

    """test if agent prevents opponent from diagonal vertical 4-connect"""
    board_l_d = generate_win_board(DIAGONAL, PLAYER2, apply_last_action=False, block_opponent_win=True)
    # print(pretty_print_board(board_l_d))
    action = mcts_algorithm(board_l_d, PLAYER1)
    board_l_d = apply_player_action(board_l_d, action, PLAYER1)
    board_l_d = apply_player_action(board_l_d, 5, PLAYER2)
    # print(pretty_print_board(board_l_d))
    assert not check_end_state(board_l_d, PLAYER2) == GameState.IS_WIN


def test_mcts_1order_loose():
    """test if agent prevents horizontal 4-connect of opponent"""

    board = np.array([[0, 0, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
    action = mcts_algorithm(board, PLAYER1)
    board = apply_player_action(board, action, PLAYER1)
    board = apply_player_action(board, 1, PLAYER2)
    board = apply_player_action(board, 4, PLAYER2)

    print(pretty_print_board(board))
    assert not check_end_state(board, PLAYER2) == GameState.IS_WIN

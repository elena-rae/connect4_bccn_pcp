from agents.common import *
from agents.agent_minimax.minimax import get_valid_columns

""" functions for generating different board types"""

Orientation = np.int8
HORIZONTAL = Orientation(0)
VERTICAL = Orientation(1)
DIAGONAL = Orientation(2)


def generate_draw_board():
    """generate a board with GameSTate.IS_DRAW"""
    board_draw = np.array([[1, 1, 2, 2, 1, 1, 2], [1, 1, 2, 2, 1, 1, 2], [2, 2, 1, 1, 2, 2, 1], [1, 1, 2, 2, 1, 1, 2],
                           [1, 1, 2, 2, 1, 1, 2], [1, 1, 1, 2, 1, 2, 2]])
    return board_draw


def generate_win_board(direction: Orientation, player: BoardPiece, apply_last_action=True, block_opponent_win=False):
    """
    Generate 1st order win/loose boards
    Parameters
    -----------
    direction: Orientation of the connect-4 [HORIZONTAL, VERTICAL, DIAGONAL]
    player: player for which the last action should be applied
    apply_last_action=True: the generated board is already won by player
    block_opponent_win=True: the opponents winning option is blocked
    Return:
    -----------
    win_board: board with the desired connect4 configuration
    """
    if direction == HORIZONTAL:
        win_board = np.array([[1, 0, 1, 1, 2, 2, 1], [0, 0, 0, 2, 2, 0, 2], [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])

    if direction == VERTICAL:
        win_board = np.array([[1, 1, 2, 2, 1, 2, 1], [0, 1, 0, 0, 0, 2, 0], [0, 1, 0, 0, 0, 2, 0],
                              [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])

    if direction == DIAGONAL:
        win_board = np.array([[1, 1, 2, 2, 1, 2, 1], [0, 2, 2, 1, 2, 2, 1], [0, 1, 1, 0, 0, 0, 1],
                              [0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])

    """ if apply_last_action, function returns a board where the game is already won"""
    if apply_last_action:
        if player == PLAYER1:
            apply_player_action(win_board, 1, PLAYER1)
        if player == PLAYER2:
            apply_player_action(win_board, 5, PLAYER2)

    """if block_opponent_win the winning option of the opponent is blocked """
    if block_opponent_win:
        if player == PLAYER1:
            apply_player_action(win_board, 5, PLAYER1)
        if player == PLAYER2:
            apply_player_action(win_board, 1, PLAYER2)

    return win_board


""" Tests for the connect4 common module """


def test_initialize_game_state():
    ret = initialize_game_state()

    assert isinstance(ret, np.ndarray)  # returns True if the object (ret) is an instance of argument (here np.ndarray)
    assert ret.dtype == BoardPiece  #
    assert ret.shape == (6, 7)
    assert np.all(ret == NO_PLAYER)
    print(ret)


def test_pretty_print_and_string_to_board():
    board = generate_draw_board()
    # print(board)
    board_in = pretty_print_board(board)
    # print(pretty_print_board(board))
    board_out = string_to_board(board_in)

    assert board.all() == board_out.all()


def test_apply_player_action():

    """test if valid action is applied correctly """
    board = initialize_game_state()
    action = np.random.choice(get_valid_columns(board))
    new_board = apply_player_action(board, action, PLAYER1)
    assert new_board[0, action] == PLAYER1
    """test if action with invalid player is not applied"""
    invalid_player = 3
    new_board_i = apply_player_action(board, action, invalid_player)
    assert new_board.all() == new_board_i.all()

    """test if action with invalid column is not applied"""
    invalid_action = 7
    new_board_i = apply_player_action(board, invalid_action, PLAYER1)
    assert new_board.all() == new_board_i.all()


def test_check_end_state():
    """test if check_end_state function gives correct output for different inputs"""

    """"check if GameState.IS_DRAW is returned correctly """
    draw_board = generate_draw_board()
    # print(pretty_print_board(draw_board))
    assert check_end_state(draw_board, PLAYER2) == GameState.IS_DRAW

    """"check if GameState.IS_WIN and GameState.Still_Playing is returned correctly """
    board_win_p1 = generate_win_board(VERTICAL, PLAYER1)
    # print(pretty_print_board(board_win_p1))
    assert check_end_state(board_win_p1, PLAYER2) == GameState.STILL_PLAYING
    assert check_end_state(board_win_p1, PLAYER1) == GameState.IS_WIN

    board_win_p2 = generate_win_board(VERTICAL, PLAYER2)
    # print(pretty_print_board(board_win_p2))
    assert check_end_state(board_win_p2, PLAYER1) == GameState.STILL_PLAYING
    assert check_end_state(board_win_p2, PLAYER2) == GameState.IS_WIN

    board_win_p1 = generate_win_board(HORIZONTAL, PLAYER1)
    # print(pretty_print_board(board_win_p1))
    assert check_end_state(board_win_p1, PLAYER2) == GameState.STILL_PLAYING
    assert check_end_state(board_win_p1, PLAYER1) == GameState.IS_WIN

    board_win_p2 = generate_win_board(HORIZONTAL, PLAYER2)
    # print(pretty_print_board(board_win_p2))
    assert check_end_state(board_win_p2, PLAYER1) == GameState.STILL_PLAYING
    assert check_end_state(board_win_p2, PLAYER2) == GameState.IS_WIN

    board_win_p1 = generate_win_board(DIAGONAL, PLAYER1)
    # print(pretty_print_board(board_win_p1))
    assert check_end_state(board_win_p1, PLAYER2) == GameState.STILL_PLAYING
    assert check_end_state(board_win_p1, PLAYER1) == GameState.IS_WIN

    board_win_p2 = generate_win_board(DIAGONAL, PLAYER2)
    # print(pretty_print_board(board_win_p2))
    assert check_end_state(board_win_p2, PLAYER1) == GameState.STILL_PLAYING
    assert check_end_state(board_win_p2, PLAYER2) == GameState.IS_WIN

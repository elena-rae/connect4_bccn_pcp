import numpy as np
from agents.common import BoardPiece, NO_PLAYER, initialize_game_state


def test_initialize_game_state():
    ret = initialize_game_state()

    assert isinstance(ret, np.ndarray) #returns True if the object (ret) is an instance of argument (here np.ndarray)from agents.common import initialize_game_state
    assert ret.dtype == BoardPiece #
    assert ret.shape == (6, 7)
    assert np.all(ret == NO_PLAYER)
    print(ret)


def test_pretty_print_board():
    from agents.common import pretty_print_board, apply_player_action
    board = initialize_game_state()
    for x in range(5):
        apply_player_action(board, x, 1)
    apply_player_action(board, 6, 2)

    print(pretty_print_board(board))



def test_string_to_board():
    from agents.common import pretty_print_board, apply_player_action, string_to_board
    board = initialize_game_state()

    for x in range(5):
        apply_player_action(board, x, 1)
    for y in range(1,6,2):
        apply_player_action(board, y, 2)

    board_in = pretty_print_board(board)

    board_out = string_to_board(board_in)

    assert board.all() == board_out.all()

def test_check_end_state():
    from agents.common import apply_player_action, pretty_print_board, check_end_state, GameState
    """"check if GameState.IS_DRAW is returned correctly """
    board_draw = initialize_game_state()

    for row in range(2):
        for x in (0, 1 ,4 ,5):
            apply_player_action(board_draw, x, 1)
        for o in (2,3,6):
            apply_player_action(board_draw, o, 2)

    for row in range(1):
        for x in (2, 3, 6):
            apply_player_action(board_draw, x, 1)
        for o in (0, 1, 4, 5):
            apply_player_action(board_draw, o, 2)

    for row in range(2):
        for x in (0, 1 ,4 ,5):
            apply_player_action(board_draw, x, 1)
        for o in (2, 3, 6):
            apply_player_action(board_draw, o, 2)

    for row in range(1):
        for x in (0, 1, 2, 4):
            apply_player_action(board_draw, x, 1)
        for o in ( 3, 5,6):
            apply_player_action(board_draw, o, 2)

    print(pretty_print_board(board_draw))
    print(check_end_state(board_draw,2))
    assert check_end_state(board_draw,2) == GameState.IS_DRAW
    print()

    """"check if GameState.IS_WIN is returned correctly """
    board_win = initialize_game_state()

    for row in range(4):
        for x in (0, 1, 4, 5):
            apply_player_action(board_win, x, 1)
        for o in (2, 3, 6):
            apply_player_action(board_win, o, 2)


    print(pretty_print_board(board_win))
    assert check_end_state(board_win, 2) == GameState.IS_WIN
    print(check_end_state(board_win, 2))
    print()

    """"check if GameState.STILL_PLAYING is returned correctly """
    board_sp = initialize_game_state()

    for row in range(3):
        for x in (0, 1, 4, 5):
            apply_player_action(board_sp, x, 1)
        for o in (2, 3, 6):
            apply_player_action(board_sp, o, 2)

    print(pretty_print_board(board_sp))
    assert check_end_state(board_sp, 2) == GameState.STILL_PLAYING
    print(check_end_state(board_sp, 2))

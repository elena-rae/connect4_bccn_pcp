import numpy as np
from agents.agent_minimax.minimax import *
from agents.agent_random.random import generate_move_random
from agents.common import *

def test_get_valid_column():
    board = initialize_game_state()
    for x in range(5):
        apply_player_action(board, x, 1)
    print(pretty_print_board(board))

    valid_columns = get_valid_columns(board)
    print("valid columns", valid_columns)
    assert len(valid_columns) == 7

    print()
    for x in range(5):
        for y in range(1,6,2):
            apply_player_action(board, y, 2)
    print(pretty_print_board(board))

    valid_columns = get_valid_columns(board)
    print("valid columns", valid_columns)
    assert len(valid_columns) == 5


def test_evaluate_board():
    board = initialize_game_state()
    """assert horizontal evaluation"""
    for x in range(3):
        apply_player_action(board, x+2, 1)
    for x in range(2):
        apply_player_action(board, x+2, 2)

    print(pretty_print_board(board))
    score_player1 = evaluate_board(board, 1)
    assert score_player1 > 0

    score_player2 = evaluate_board(board, 2)
    assert score_player2 < 0

    """assert vertical evaluation """
    for x in range(3):
        apply_player_action(board, 4, 2)
    print(pretty_print_board(board))
    score_player2 = evaluate_board(board, 2)
    assert score_player2 > 0




def test_is_terminal_node():
    """"""
    """"check is_terminal_node for final node GameState.IS_DRAW """
    board_draw = initialize_game_state()

    for row in range(2):
        for x in (0, 1, 4, 5):
            apply_player_action(board_draw, x, 1)
        for o in (2, 3, 6):
            apply_player_action(board_draw, o, 2)

    for row in range(1):
        for x in (2, 3, 6):
            apply_player_action(board_draw, x, 1)
        for o in (0, 1, 4, 5):
            apply_player_action(board_draw, o, 2)

    for row in range(2):
        for x in (0, 1, 4, 5):
            apply_player_action(board_draw, x, 1)
        for o in (2, 3, 6):
            apply_player_action(board_draw, o, 2)

    for row in range(1):
        for x in (0, 1, 2, 4):
            apply_player_action(board_draw, x, 1)
        for o in (3, 5):
            apply_player_action(board_draw, o, 2)

    print(pretty_print_board(board_draw))
    assert is_terminal_node(board_draw,6) is True
    print("next action at position 6")
    print()

    """"check is_terminal_node for final node GameState.IS_WIN is True """
    board_win = initialize_game_state()

    for row in range(3):
        for x in (0, 1, 4, 5):
            apply_player_action(board_win, x, 1)
        for o in (2, 3):
            apply_player_action(board_win, o, 2)

    print(pretty_print_board(board_win))

    assert is_terminal_node(board_win, 5) is True
    print("next action at position 5")
    print(is_terminal_node(board_win, 5))

    """"check is_terminal_node for final node GameState.Still_playing is False """

    assert is_terminal_node(board_win, 6) is False
    print("next action at position 5")
    print(is_terminal_node(board_win, 6))
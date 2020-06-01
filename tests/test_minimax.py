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
    """"""
    """assert horizontal evaluation"""
    board = initialize_game_state()
    for x in range(3):
        apply_player_action(board, x+2, 1)

    score_player1= evaluate_board(board, 1)
    #print(pretty_print_board(board))
    assert score_player1 > 0

    for x in range(2):
        apply_player_action(board, x+2, 2)

    score_player2 = evaluate_board(board, 2)
    score_player1= evaluate_board(board, 1)

    #print(pretty_print_board(board))
    assert score_player2 == -score_player1


    """assert vertical evaluation """
    board = initialize_game_state()
    for x in range(3):
        apply_player_action(board, 3, 1)

    score_player1 = evaluate_board(board, 1)
    assert score_player1 > 0

    for x in range(3):
        apply_player_action(board, 5, 2)

    score_player2 = evaluate_board(board, 2)
    score_player1 = evaluate_board(board, 1)
    #print(pretty_print_board(board))

    assert score_player2 == -score_player1

    """assert diagonal evaluation positiv slope """
    board = initialize_game_state()
    for x in range(2):
        apply_player_action(board, x + 4, 2)
    for x in range(3):
        apply_player_action(board, x + 3, 1)

    score_player1 = evaluate_board(board, 1)
    score_player2 = evaluate_board(board, 2)
    #print(pretty_print_board(board))
    assert score_player1 > 0
    assert score_player2 < 0


    """assert diagonal evaluation negative slope """
    board = initialize_game_state()
    apply_player_action(board, 2, 2)
    for x in range(2):
        apply_player_action(board, x+2, 1)
    for x in range(3):
        apply_player_action(board, x+2, 2)

    score_player1 = evaluate_board(board, 1)
    score_player2 = evaluate_board(board, 2)
    #print(pretty_print_board(board))
    assert score_player1 < 0
    assert score_player2 > 0

def test_evaluate_window():
    pass

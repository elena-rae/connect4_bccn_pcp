import numpy as np
from agents.agent_random.random import generate_move_random
from agents.common import *


def test_generate_random_move():
    saved_state = {PLAYER1: None, PLAYER2: None}

    """ test if an empty column is found: """
    board = initialize_game_state()

    for row in range(3):
        for x in range(6):
            apply_player_action(board, x, 1)
        for o in range(6):
            apply_player_action(board, o, 2)
    print(pretty_print_board(board))
    action, saved_state = generate_move_random(board, 1, saved_state)
    assert action == 6



import numpy as np
from connectn.common import BoardPiece, NO_PLAYER, initialize_game_state



def test_initialize_game_state():
    from connectn.common import initialize_game_state

    ret = initialize_game_state()

    assert isinstance(ret, np.ndarray) #returns True if the object (ret) is an instance of argument (here np.ndarray)from connectn.common import initialize_game_state
    assert ret.dtype == BoardPiece #
    assert ret.shape == (6, 7)
    assert np.all(ret == NO_PLAYER)


def test_pretty_print_board():
    from connectn.common import pretty_print_board
    board = initialize_game_state()
    ret = pretty_print_board(board)

    assert ret.dtype == str


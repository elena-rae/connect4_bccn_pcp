import numpy as np
from agents.common import *

def generate_move_random(
    board: np.ndarray, saved_state: Optional[SavedState]
) -> Tuple[PlayerAction, Optional[SavedState]]:
    """return a randomly chosen valid column as `action`
    Parameters
    -----------
    board: np.ndarray
        board reflecting current game state
    Return
    -----------
    action: int
    """

    #check if board is already full
    if np.all(board != 0) == True:
        print("Error-generating_random_move, board is full")
        return -1, saved_state

    action = np.random.randint(0,7,1)

    while board[5,action] != 0:
        action = np.random.randint(0, 7, 1)

    return action, saved_state


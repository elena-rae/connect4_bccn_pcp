import numpy as np
from enum import Enum
from typing import Optional

from numpy.core._multiarray_umath import ndarray

BoardPiece = np.int8  # The data type (dtype) of the board
NO_PLAYER = BoardPiece(0)  # board[i, j] == NO_PLAYER where the position is empty
PLAYER1 = BoardPiece(1)  # board[i, j] == PLAYER1 where player 1 has a piece
PLAYER2 = BoardPiece(2)  # board[i, j] == PLAYER2 where player 2 has a piece

PlayerAction = np.int8  # The column to be played


class GameState(Enum):
    IS_WIN = 1
    IS_DRAW = -1
    STILL_PLAYING = 0


def initialize_game_state() -> np.ndarray:
    """Returns an ndarray, shape (6, 7) and data type (dtype) BoardPiece, initialized to 0 (NO_PLAYER). """
    return np.zeros((6, 7), dtype=BoardPiece)


def pretty_print_board(board: np.ndarray) -> str:
    """ return `board` converted to a human readable string representation,
        to be used when playing or printing diagnostics to the console (stdout). The piece in
        board[0, 0] should appear in the lower-left."""

    """define strings for the general layout of the output"""
    pretty_numbering = str("| 0 1 2 3 4 5 6 |")
    pretty_line = str("|===============|")

    """ flip board array and transform into string change array values into symbols (x,o), 
        raise error for invalid values in board array """
    pretty_board = np.flipud(board.astype(str))

    for row in range(len(pretty_board)):
        for elem in range(len(pretty_board[row])):
            if pretty_board[row, elem] == '0':
                pretty_board[row, elem] = " "
            elif pretty_board[row, elem] == "1":
                pretty_board[row, elem] = "x"
            elif pretty_board[row, elem] == "2":
                pretty_board[row, elem] = "o"
            else:
                print("Invalid Input")
                return 0

    """ generate the strings for each row of the board array"""
    print(pretty_line)

    for row in pretty_board:
        print("|", ' '.join([str(elem) for elem in row]), "|")

    print(pretty_line)
    print(pretty_numbering)
    return (pretty_board)


def string_to_board(pp_board: str) -> np.ndarray:
    """
    Takes the output of pretty_print_board and turns it back into an ndarray.
    This is quite useful for debugging, when the agent crashed and you have the last
    board state as a string.
    """
    raise NotImplemented()


def apply_player_action(
        board: np.ndarray, action: PlayerAction, player: BoardPiece, copy: bool = False
) -> np.ndarray:
    """
    Sets board[i, action] = player, where i is the lowest open row. The modified
    board is returned. If copy is True, makes a copy of the board before modifying it.
    """
    if copy:
        oldboard = board

    if 0 <= action <= 6 is False:
        print("Choose a column for your action (0-6)")
    if 1 <= player <= 2 is False:
        print("Which Player? (Player1 -> 1, Player2 -> 2")

    for row in range(0, 6):
        if board[row, action] == 0:
            board[row, action] = player
            break

        if row == 5:
            print("Oops, column is already full!")
            break

    if copy:
        return board, oldboard
    else:
        return board


def connected_four(
        board: np.ndarray, player: BoardPiece, last_action: Optional[PlayerAction] = None,
) -> bool:
    """
    Returns True if there are four adjacent pieces equal to `player` arranged
    in either a horizontal, vertical, or diagonal line. Returns False otherwise.
    If desired, the last action taken (i.e. last column played) can be provided
    for potential speed optimisation.
    """

    """ check if input /last action is legit"""
    if player == 0:
        print("No previous player action")
        return False

    """ find out the row of last action"""
    for row in range(0, 6):
        if board[row, last_action] == 0:
            last_row = row - 1
            break
        if row == 5:
            last_row = 5
    print("last (row, column) (", last_row, ",", last_action, ")")

    count = 0  # counter for evaluating number of neighbouring pieces

    """ search horizontally to right (increasing column nr) """
    for step in range(0, 3):
        step = step + 1
        print(step, "to right")
        if last_action + step <= 6:
            if board[last_row, last_action + step] == player:
                count = count + 1
                print("count", count)
            else:
                print("nothing right")
                break
        else:
            print("right over board")
            break
    """ search horizontally to left (decreasing column nr) """
    for step in range(0, 3):
        step = step + 1
        print(step, "to left")
        if last_action - step >= 0:
            if board[last_row, last_action - step] == player:
                count = count + 1
                print("count", count)
            else:
                print("nothing left")
                break
        else:
            print("left over board")
            break

    """ check if horizontal connect four is achieved, if not reset counter"""
    if count >= 3:
        print("4 connected, Player {} won!".format(player))
        return True
    else:
        count = 0

    """search vertically down the column (decreasing row nr)"""
    for step in range(0, 3):
        step = step + 1
        print(step, "down")
        if last_row - step >= 0:
            if board[last_row - step, last_action] == player:
                count = count + 1
                print("count", count)
            else:
                print("wrong piece")
                break
        else:
            print("down over board")
            break

    """check if vertical connect four is achieved, if not reset counter  """
    if count >= 3:
        print("4 connected, Player {} won!".format(player))
        return True
    else:
        count = 0

    """ search diagonal to upper right (increasing column nr, increasing row nr) """
    for step in range(0, 3):
        step = step + 1
        print(step, "to up right")
        if last_action + step <= 6 and last_row + step <=5:
            if board[last_row + step, last_action + step] == player:
                count = count + 1
                print("count", count)
            else:
                print("nothing up right")
                break
        else:
            print("up right over board")
            break
    """ search diagonal to lower left (decreasing column nr, decreasing row nr) """
    for step in range(0, 3):
        step = step + 1
        print(step, "to lower left")
        if last_action - step >= 0 and last_row - step >= 0:
            if board[last_row - step, last_action - step] == player:
                count = count + 1
                print("count", count)
            else:
                print("nothing lower left")
                break
        else:
            print("lower left over board")
            break

    """check if diagonal (lower left to upper right) connect four is achieved, if not reset counter  """
    if count >= 3:
        print("4 connected, Player {} won!".format(player))
        return True
    else:
        count = 0

        print("next player continue!")
        return False


def check_end_state(
        board: np.ndarray, player: BoardPiece, last_action: Optional[PlayerAction] = None,
) -> GameState:
    """
    Returns the current game state for the current `player`, i.e. has their last
    action won (GameState.IS_WIN) or drawn (GameState.IS_DRAW) the game,
    or is play still on-going (GameState.STILL_PLAYING)?
    """
    raise NotImplemented()


""" next week

def human_vs_agent(
        generate_move_1: cu.GenMove,
        generate_move_2: cu.GenMove = user_move,
        player_1: str = "Player 1",
        player_2: str = "Player 2",
        args_1: tuple = (),
        args_2: tupla = (),
        init_1: Callable = lambda board, player: None,
        init_2: Callable = lambda board, player: None,
):
    pass
"""

import numpy as np
from enum import Enum
import copy
from typing import Optional, Callable, Tuple
# from numpy.core._multiarray_umath import ndarray


class SavedState:
    pass


class GameState(Enum):
    IS_WIN = 1
    IS_DRAW = -1
    STILL_PLAYING = 0


BoardPiece = np.int8  # The data type (dtype) of the board
NO_PLAYER = BoardPiece(0)  # board[i, j] == NO_PLAYER where the position is empty
PLAYER1 = BoardPiece(1)  # board[i, j] == PLAYER1 where player 1 has a piece
PLAYER2 = BoardPiece(2)  # board[i, j] == PLAYER2 where player 2 has a piece

PlayerAction = np.int8  # The column to be played

GenMove = Callable[
        [np.ndarray, BoardPiece, Optional[SavedState]],  # Arguments for the generate_move function
        Tuple[PlayerAction, Optional[SavedState]]  # Return type of the generate_move function
        ]


def initialize_game_state() -> np.ndarray:
    """Returns an ndarray, shape (6, 7) and data type (dtype) BoardPiece, initialized to 0 (NO_PLAYER). """
    return np.zeros((6, 7), dtype=BoardPiece)


def pretty_print_board(board: np.ndarray) -> str:
    """ return `board` converted to a human readable string representation,
        to be used when playing or printing diagnostics to the console (stdout). The piece in
        board[0, 0] should appear in the lower-left."""
    """ flip board array and transform into string,  
    change array values into symbols (x,o), raise error for invalid values in board array """
    flipped_board = np.flipud(board.astype(str))

    for r, row in enumerate(flipped_board):
        for c, elem in enumerate(row):
            if flipped_board[r, c] == '0':
                flipped_board[r, c] = " "
            elif flipped_board[r, c] == "1":
                flipped_board[r, c] = "x"
            elif flipped_board[r, c] == "2":
                flipped_board[r, c] = "o"
            else:
                return "Invalid Input"

    pretty_board = ["|===============|"]

    """ generate and add the strings for each row of the board array"""
    for row in flipped_board:
        joined_row = ' '.join(row)
        joined_row = "| " + joined_row + " |"
        pretty_board.append(joined_row)

    pretty_board.append("|===============|")
    pretty_board.append("| 0 1 2 3 4 5 6 |")
    pretty_board = "\n".join(pretty_board)

    return pretty_board


def string_to_board(pp_board: str) -> np.ndarray:
    """
    Takes the output of pretty_print_board and turns it back into an ndarray.
    This is quite useful for debugging, when the agent crashed and you have the last
    board state as a string.
    """
    board_as_array = np.zeros((6, 7), dtype=BoardPiece)

    """transform string to array for better handling"""
    board = np.array(list(pp_board))
    """remove newlines comands from string, and reshape back to row x columns and remove pretty boarders"""
    newline_indices = np.argwhere(board == "\n")
    board = np.delete(board, newline_indices)
    board = board.reshape((9, 17))
    boarder_indices = [0, 7, 8]
    board = np.delete(board, boarder_indices, 0)

    """ remove surplus gaps, for every x place 1 and every o place 2 the initialized 0-array  """
    gap_indices = (0, 1, 3, 5, 7, 9, 11, 13, 15, 16, 17)

    for r, row in enumerate(board):
        string_to_int = np.delete(row, gap_indices)
        x_indices = np.argwhere(string_to_int == "x")
        board_as_array[r, x_indices] = 1
        o_indices = np.argwhere(string_to_int == "o")
        board_as_array[r, o_indices] = 2

    """flip and return the array"""
    board_as_array = np.flipud(board_as_array)
    return board_as_array


def apply_player_action(board: np.ndarray, action: PlayerAction, player: BoardPiece, copying=False) -> np.ndarray:
    """
    Sets board[i, action] = player, where i is the lowest open row. The modified
    board is returned. If copy is True, makes a copy of the board before modifying it.
    """
    if copying:
        board = copy.copy(board)

    if 0 <= action <= 6 is False:
        print('Pick a column for your action (0-6)')
    if 1 <= player <= 2 is False:
        print('Which Player? (Player1 -> 1, Player2 -> 2')

    for row in range(0, 6):
        if board[row, action] == 0:
            board[row, action] = player
            break

        if row == 5:
            break

    return board


def connected_four(
    board: np.ndarray, player: BoardPiece, _last_action: Optional[PlayerAction] = None, connect_n=4
) -> bool:
    """
    search board for connect_n pieces in a row, if this is the case return True
    """

    rows, cols = board.shape
    rows_edge = rows - connect_n + 1
    cols_edge = cols - connect_n + 1
    for i in range(rows):
        for j in range(cols_edge):
            if np.all(board[i, j:j + connect_n] == player):
                return True
    for i in range(rows_edge):
        for j in range(cols):
            if np.all(board[i:i + connect_n, j] == player):
                return True
    for i in range(rows_edge):
        for j in range(cols_edge):
            block = board[i:i + connect_n, j:j + connect_n]
            if np.all(np.diag(block) == player):
                return True
            if np.all(np.diag(block[::-1, :]) == player):
                return True
    return False


def check_end_state(board: np.ndarray, player: BoardPiece, last_action: Optional[PlayerAction] = None) -> GameState:
    """
    Returns the current game state for the current `player`, i.e. has their last
    action won (GameState.IS_WIN) or drawn (GameState.IS_DRAW) the game,
    or is play still on-going (GameState.STILL_PLAYING)?
    """
    if connected_four(board, player, last_action) is True:
        return GameState.IS_WIN

    if np.any(board == 0):
        return GameState.STILL_PLAYING

    if np.all(board != 0):
        return GameState.IS_DRAW

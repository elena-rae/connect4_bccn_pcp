import numpy as np
from agents.common import *

MINIMAX_DEPTH = 2


def minimax(
        board: np.ndarray, depth: MINIMAX_DEPTH, maximizingTrue  # PlayerToBeMaximized: BoardPiece,
):
    """some general minimax algorithm description"""

    valid_columns = get_valid_columns(board)
    best_column = np.random.choice(valid_columns, 1)
    """Edge Case: (terminal node) AI or Player is winning with the next piece or the board is full (draw)"""

    is_terminal, terminal_result, winning_column, winning_player = is_terminal_node(board, valid_columns)
    if depth == 0 or is_terminal == True:
        if is_terminal:
            if terminal_result == GameState.IS_WIN and winning_player == PLAYER2:
                return winning_column, 100000000000
            elif terminal_result == GameState.IS_WIN and winning_player == PLAYER1:
                return winning_column, -100000000000
            elif terminal_result == GameState.IS_DRAW:  # Game over because draw (no valid moves)
                return winning_column, None

        else:  # case where depth = 0
            heuristic_value_for_next_move = evaluate_board(board, PLAYER2)  ### player needs to be AI
            return None, heuristic_value_for_next_move

    """ recursive minimizing/maximizing case"""
    if maximizingTrue:
        value = -np.inf

        for column in valid_columns:
            c_board = board.copy()
            apply_player_action(c_board, column, PLAYER2)  ### player needs to be AI
            new_score = minimax(c_board, depth - 1, False)[
                1]  ### maximizingTrue is False for next iter, because  will not be AI
            if new_score > value:
                value = new_score
                best_column = column
        return best_column, value
    else:  # minimizing player case
        value = np.inf
        for column in valid_columns:
            c_board = board.copy()
            apply_player_action(c_board, column, PLAYER1)  ### player needs to be minimizing player
            new_score = minimax(c_board, depth - 1, True)[
                1]  ### maximizingTrue is True for next iter, because will be AI
            if new_score < value:
                value = new_score
                best_column = column
        return best_column, value


def is_terminal_node(
        board: np.ndarray, valid_columns: np.ndarray
) -> Tuple[bool, GameState, int, BoardPiece]:
    """check if one possible action leads to either AI or PLAYER winning or draw
    (player performing the action is not specified
    :param board:
    :param valid_columns:
    :return: """
    for column in valid_columns:
        board_after_PLAYER1_action = board.copy()
        board_after_PLAYER1_action = apply_player_action(board_after_PLAYER1_action, column, PLAYER1)

        if check_end_state(board_after_PLAYER1_action, PLAYER1) != GameState.STILL_PLAYING:
            return True, check_end_state(board_after_PLAYER1_action, PLAYER1), column, PLAYER1

        board_after_PLAYER2_action = board.copy()
        board_after_PLAYER2_action = apply_player_action(board_after_PLAYER2_action, column, PLAYER2)

        if check_end_state(board_after_PLAYER2_action, PLAYER2) != GameState.STILL_PLAYING:
            return True, check_end_state(board_after_PLAYER2_action, PLAYER2), column, PLAYER2

    else:
        return False, GameState.STILL_PLAYING, None, None


def get_valid_columns(board: np.ndarray) -> ndarray:
    """return list of all columns with possible valid moves """
    valid_columns_array = []
    for m, col in enumerate(board.T):
        for n, row in enumerate(col):
            if board.T[m, n] == 0:
                valid_columns_array.append(m)
                break
    return valid_columns_array


def evaluate_window(window: np.ndarray, player: BoardPiece) -> int:
    """ evaluate a window (fraction of the board) passed into the function by evaluate_board """
    window_score = 0
    if player == PLAYER1:
        opponent = PLAYER2
    elif player == PLAYER2:
        opponent = PLAYER1

    """Raise score if Player has 2 or more pieces in a window"""
    if sum(window == player) == 4:
        window_score += 100
    elif sum(window == player) == 3 and sum(window == NO_PLAYER) == 1:
        window_score += 5
    elif sum(window == player) == 2 and sum(window == NO_PLAYER) == 2:
        window_score += 2

    """penalty if opponent hast 3 pieces in a window with an empty space next to it"""
    if sum(window == opponent) == 3 and sum(window == NO_PLAYER) == 1:
        window_score -= 10
    return window_score


def evaluate_board(
        board: np.ndarray, player: BoardPiece
) -> int:
    """return a score reflecting the state of the board for the given player"""
    WINDOW_LENGTH = 4
    board_score = 0
    n_rows, m_columns = board.shape

    """evaluate horizontally """
    for r, row in enumerate(board):
        for c in range(m_columns - 3):
            window = row[c:c + WINDOW_LENGTH]
            board_score += evaluate_window(window, player)

    """evaluate horizontally """
    tboard = np.transpose(board)
    for r, trow in enumerate(tboard):
        for c in range(n_rows - 3):
            twindow = trow[c:c + WINDOW_LENGTH]
            board_score += evaluate_window(twindow, player)

    """ TODO diagonal evaluation """

    """increase score for player pieces in the central column"""
    central_column = int(m_columns / 2 + 0.5)
    centercount = sum(tboard[central_column] == player)
    board_score += centercount * 5
    return board_score


def pick_smart_move(
        board: np.ndarray, player: BoardPiece, saved_state: Optional[SavedState]
) -> Tuple[PlayerAction, Optional[SavedState]]:
    """ """
    """get all valid columns, initialize best_column at random and best_column_score =0"""
    best_column_score = 0
    valid_columns = get_valid_columns(board)
    best_column = np.random.choice(valid_columns, 1)

    """generate a hypothetical board for all possible moves and evaluate it, choose move with highest score"""
    for column in valid_columns:
        temp_board = board.copy()
        apply_player_action(temp_board, column, player)
        score = evaluate_board(temp_board, player)
        if score > best_column_score:
            best_column_score = score
            best_column = column

    return best_column, saved_state

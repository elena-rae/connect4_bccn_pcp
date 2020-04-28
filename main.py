#from connectn.agent_minimax import generate_move
from connectn.common import *

board = initialize_game_state()
board[0,0] = 2 # lower left corner of board

apply_player_action(board, 3, 2)
apply_player_action(board, 3, 2)
apply_player_action(board, 1, 2)
apply_player_action(board, 1, 2)
apply_player_action(board, 2, 2)
apply_player_action(board, 2, 2)
apply_player_action(board, 3, 2)
apply_player_action(board, 3, 2)
apply_player_action(board, 3, 1)
apply_player_action(board, 6, 2)
apply_player_action(board, 6, 2)
apply_player_action(board, 2, 2)
pretty_print_board(board)

connected_four(board, 2, 2)




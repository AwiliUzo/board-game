import sys
import time

# progam level states
test_cases_boards = [
	# e.g
	# { (0,0):"K", (0,1):".", (1,0):".", (1,1):"#" },
	# { (0,0):"K", (0,1):"#", (1,0):".", (1,1):"#", (2,0):".", (2,1):"#", (3,0):".", (3,1):"#" }
]

# case level states
ALICE = 'A'
BOB = 'B'
INIT_KING_POS = 'K'
BURNED = '#'
NOT_BURNED = '.'

board = None
king_position = None
current_player = None


def process_input(filepath):
	""" reads the inputs from the file and parses into test_cases_boards """
	global test_cases_boards

	with open(filepath) as f:
		lines = f.readlines();

		N = int(lines[0])
		case_start_line = 1
		
		for i in range(N):

			case_board = {}
			r_c = lines[case_start_line].split(" ")
			r = int(r_c[0])
			c = int(r_c[1])

			for j in range( case_start_line + 1, case_start_line + r + 1):

				row_index = j - (case_start_line + 1)
				row = lines[j]

				for col_index, column_value in enumerate(row):
					if not column_value == '\n':
						cood = (row_index, col_index)
						case_board[cood] = column_value;
			
			test_cases_boards.append(case_board)
			case_start_line += r + 1


def run_all_game_cases():
	""" runs all game cases and prints the winner/results """
	global test_cases_boards

	for index,value in enumerate(test_cases_boards):
		print("Case #%s: %s" % (index+1, run_game_case_and_get_winner(value) ) )


def run_game_case_and_get_winner(case_board):
	""" runs a game case and returns the winner """
	global board, king_position, current_player, winner

	board = case_board																# set the board for this case
	king_position = get_king_position(board)										# set the init ing_position from the board
	current_player = ALICE
	winner = None

	while True :																	# main game loop
		valid_moves = filter(is_valid_move, board.items())							# first get all the possible valid moves
		
		if len(valid_moves) > 0 : 													 
			chosen_move = get_best_move(valid_moves)								# pick the best move (a square on the board)
			execute_move(chosen_move)												# execute the move on the board
		else:																		# no more valid moves...CHECKMATE!!!
			winner = board[king_position]											# get the winner i.e the player that took/played the move to the current king_position
			break

	if winner == INIT_KING_POS:
		return BOB if current_player == ALICE else ALICE
	else:
		return winner																# return the winner


def get_king_position(case_board):
	""" used to set the king_position at the start of each game case """
	for key in case_board:								
	    if case_board[key] == 'K':
	    	return key


def is_valid_move(square):
	""" test if a move to the supplied square is valid. NB: the square is a tuple e.g  ( (1,2), "#" )"""
	
	global king_position
	
	cood = square[0] 														# the coodinates of the square tuple i.e a tuple (square_row, square_column)
	state = square[1] 														# the state of the square e.g '.' for neither burned nor taken, '#' for burned , 'K' for init king_position, 'A' for taken by Alice and 'B' for taken by Bob
	
	# ensure that the square is neither more than a step away from the current king_position
	if not (king_position[0]-1) <= cood[0] <= (king_position[0]+1) : 		# horizontal test 
		return False
	if not (king_position[1]-1) <= cood[1] <= (king_position[1]+1) : 		# vertical test
		return False
	
	# ensure it is not the current king_position
	if cood[0] == king_position[0] and cood[1] == king_position[1] :	
		return False

	# ensure the square is neither burned nor taken:
	if not state == NOT_BURNED:
		return False

	# since the square passes all these validity conditions:
	return True


def get_best_move(valid_moves):
	""" returns the best move i.e one that will give your oponent the least number of valid options """
	return valid_moves[0] 													# still to be optimized


def execute_move(chosen_move):
	""" executes the chosen_move (a tuple representing a square on the board e.g ( (2,3), '#' ) """

	global board, king_position, current_player

	king_position = chosen_move[0]										# set the king_position to the chosen squares coods
	board[king_position] = current_player								# mark the king_position with the current_player value
	
	if current_player == ALICE:											# alternate/pass the turn to the othee player
		current_player = BOB
	else:
		current_player = ALICE



def main(filepath):
	""" board_game init function """
	process_input(filepath)
	run_all_game_cases()

if __name__ == "__main__":
	if len(sys.argv) > 1:												# launch main only if the input filepath is specified
		start = time.clock()
		main(sys.argv[1])
		stop = time.clock()
		print "\nThis program executed in: %s second(s)" % (stop - start)
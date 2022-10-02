"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math
from pickle import TRUE

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    empty_case = 0
    x_case = 0
    o_case = 0

    for row in board:
        for state in row:
            if state == EMPTY:
                empty_case += 1
            elif state == X:
                x_case += 1
            else:
                o_case += 1

    if empty_case == 9:
        return X

    elif x_case > o_case:
        return O

    elif x_case == o_case:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    
    count_row = 0
    count_state = 0

    for count_row, row in enumerate(board):
        for count_state, state in enumerate(row):
            #print(f"{count_row}, {count_state}")
            if state == EMPTY:
                possible_actions.add((count_row, count_state))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Whose turn it's to move.
    turn = player(board)
    # We need to make a deep copy of the board, since we can't modify the
    # original because minimax will need the original and consider these copies.
    copy_board = deepcopy(board)

    invalid_action = 0

    #Action is a tuple (i, j).
    for count_row, row in enumerate(copy_board):
        for count_state, state in enumerate(row):
            if count_row == action[0] and count_state == action[1] and state == EMPTY:
                copy_board[count_row][count_state] = turn
            else:
               invalid_action += 1

    if invalid_action == 9:
        raise ValueError("The action is not valid for this board.")
    else:
        return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    positions_x = set()
    positions_o = set()

    win_diagonally_1 = {(0,0), (1,1), (2,2)}
    win_diagonally_2 = {(0,2), (1,1), (2,0)}

    win_horizontally_1 = {(0,0), (0,1), (0,2)}
    win_horizontally_2 = {(1,0), (1,1), (1,2)}
    win_horizontally_3 = {(2,0), (2,1), (2,2)}

    win_vertically_1 = {(0,0), (1,0), (2,0)}
    win_vertically_2 = {(0,1), (1,1), (2,1)}
    win_vertically_3 = {(0,2), (1,2), (2,2)}

    # We add every postion of x and o's in their sets.
    for count_row, row in enumerate(board):
        for count_state, state in enumerate(row):
            if state == X:
                positions_x.add((count_row, count_state))
            elif state == O:
                positions_o.add((count_row, count_state))

    # We compare each set of x and o's to winning sets, if at least one 
    # winning set is present, the game ends, if not the game is in progress 
    # or ended up in a draw.
    if (set(win_diagonally_1) & set(positions_x) == win_diagonally_1 
        or set(win_diagonally_2) & set(positions_x) == win_diagonally_2
        or set(win_horizontally_1) & set(positions_x) == win_horizontally_1
        or set(win_horizontally_2) & set(positions_x) == win_horizontally_2
        or set(win_horizontally_3) & set(positions_x) == win_horizontally_3
        or set(win_vertically_1) & set(positions_x) == win_vertically_1
        or set(win_vertically_2) & set(positions_x) == win_vertically_2
        or set(win_vertically_3) & set(positions_x) == win_vertically_3):
        return X
    elif (set(win_diagonally_1) & set(positions_o) == win_diagonally_1 
        or set(win_diagonally_2) & set(positions_o) == win_diagonally_2
        or set(win_horizontally_1) & set(positions_o) == win_horizontally_1
        or set(win_horizontally_2) & set(positions_o) == win_horizontally_2
        or set(win_horizontally_3) & set(positions_o) == win_horizontally_3
        or set(win_vertically_1) & set(positions_o) == win_vertically_1
        or set(win_vertically_2) & set(positions_o) == win_vertically_2
        or set(win_vertically_3) & set(positions_o) == win_vertically_3):
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    state_game = winner(board)

    if state_game == X or state_game == O:
        return True
    elif state_game == None:
        # The winner function returns None in two cases(Draw or in process games),
        # if there's still an empty state means that it's in process, if not,
        # it means that it's a draw.
        for row in board:
            for state in row:
                if state == EMPTY:
                    return False
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    state_of_game = terminal(board)

    if state_of_game == True:
        winner_game = winner(board)
        if winner_game == X:
            return 1
        elif winner_game == O:
            return -1
        else:
            return 0
    # We assume that this function will be called if terminal(board) is False,
    # otherwise we raise an error.
    else:
       raise ValueError("terminal function is not true.")


# Added Function
def max_value(board):
    """
    Returns the value of the state if we try to maximize it.
    """
    # if max_value is called when the game is already over (all squares 
    # filled) we return whether X won, O won or it's a draw by calling utility.
    if terminal(board) == True:
        utility_board = utility(board)
        return utility_board

    possible_actions = actions(board)
    initial_value = -math.inf
    for action in possible_actions:
        initial_value = max(initial_value, min_value(result(board, action)))
    return initial_value


# Added Function
def min_value(board):
    """
    Returns the value of the state if we try to minimize it.
    """
    # if min_value is called when the game is already over (all squares 
    # filled) we return whether X won, O won or it's a draw by calling utility.
    if terminal(board) == True:
        utility_board = utility(board)
        return utility_board

    possible_actions2 = actions(board)
    initial_value2 = math.inf
    for action in possible_actions2:
        initial_value2 = min(initial_value2, max_value(result(board, action)))
    return initial_value2
      

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    state_of_game = terminal(board)

    if state_of_game == True:
        return None
    else:
        player_turn = player(board)

        if player_turn == X:
            # The x player picks an action in the possible set of actions that
            # gives the highest value of min_value of the resultant board when
            # one of these actions is applied.(min_value(result(board, action)).
            possible_actions_x = actions(board)
            
            highest_value = -math.inf

            for action in possible_actions_x:
                resultant_board = result(board, action)
                value_minimized = min_value(resultant_board)
                # We need to keep track of the best actions as the algorithm
                # loops through all of them.
                if value_minimized > highest_value:
                    highest_value = value_minimized
                    best_action = action

            return best_action

        else:
            # The o player picks an action in the possible set of actions that
            # gives the smallest value of max_value of the resultant board when
            # one of these actions is applied.(max_value(result(board, action)).
            possible_actions_o = actions(board)
            
            smallest_value = math.inf

            for action in possible_actions_o:
                resultant_board = result(board, action)
                value_maximized = max_value(resultant_board)
                # We need to keep track of the best actions as the algorithm
                # loops through all of them.
                if value_maximized < smallest_value:
                    smallest_value = value_maximized
                    best_action = action

            return best_action



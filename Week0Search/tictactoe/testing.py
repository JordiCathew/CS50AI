"""
¡Tests functions to know if they work properly!
"""

#from CS50AI.Week0Search.tictactoe.tictactoe import utility
from tictactoe import (player, actions, result, winner, terminal, utility, 
                      max_value, min_value, minimax)

X = "X"
O = "O"
EMPTY = None
board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, X, EMPTY],
         [EMPTY, EMPTY, EMPTY]]

action = (2, 2)

def testing_player(board):
    result = player(board)
    print("Is the turn of player: " + result)

def testing_actions(board):
    print(board)
    result2 = actions(board)
    print(result2)

def testing_result(board, action):
    print(board)
    result3 = result(board, action)
    print(result3)

def testing_winner(board):
    print(board)
    result4 = winner(board)
    print(result4)

def testing_terminal(board):
    print(board)
    result5 = terminal(board)
    print(result5)

def testing_utility(board):
    print(board)
    result6 = utility(board)
    print(result6)

def testing_max(board):
    print(board)
    result7 = max_value(board)
    print(result7)

def testing_min(board):
    print(board)
    result8 = min_value(board)
    print(result8)

def testing_minimax(board):
    print(board)
    result9 = minimax(board)
    print(result9)

#testing_player(board)
#testing_actions(board)
#testing_result(board, action)
#testing_winner(board)
#testing_terminal(board)
#testing_utility(board)
#testing_min(board)
testing_minimax(board)

"""
¡Tests functions to know if they work properly!
"""

from tictactoe import player, actions

X = "X"
O = "O"
EMPTY = None
board = [[X, EMPTY, O],
        [EMPTY, X, EMPTY],
        [EMPTY, EMPTY, EMPTY]]

def testing_player(board):
    result = player(board)
    print(result)

def testing_actions(board):
    result2 = actions(board)
    print(result2)

testing_player(board)
testing_actions(board)

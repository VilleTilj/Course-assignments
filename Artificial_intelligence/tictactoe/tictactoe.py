"""
Tic Tac Toe Player
"""

import math
import copy

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
    nones = board[0].count(None) + board[1].count(None) + board[2].count(None)
    xs = board[0].count(X) + board[1].count(X) + board[2].count(X)
    os = board[0].count(O) + board[1].count(O) + board[2].count(O)

    if nones == 9:
        return X
    elif os == xs:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    to_Return = set()

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if (board[i][j] != X) and (board[i][j] != O):
                to_Return.add((i, j))

    return to_Return


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    tempBoard = copy.deepcopy(board)
    if tempBoard[action[0]][action[1]] == X or tempBoard[action[0]][action[1]] == O:
        raise Exception
    else:
        actor = player(tempBoard)
        tempBoard[action[0]][action[1]] = actor
        return tempBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        # Check horizontal lines
        if (board[i][0] == board[i][1] == board[i][2]) and (board[i][0] != EMPTY):
            return board[i][0]
        # check vertical lines
        if (board[0][i] == board[1][i] == board[2][i]) and (board[0][i] != EMPTY):
            return board[0][i]

        # Check diagonals
    if (board[0][0] == board[1][1] == board[2][2]) or (board[0][2] == board[1][1] == board[2][0]) \
            and board[1][1] != EMPTY:
        return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None or  board[0].count(None) + board[1].count(None) + board[2].count(None) == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    won = winner(board)

    if won == X:
        return 1
    if won == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    best_action = None
    if terminal(board):
        return None

    elif player(board) == X:
        temp = -math.inf
        for action in actions(board):
            min_val = min_node(result(board, action))

            if min_val > temp:
                temp = min_val
                best_action = action

    elif player(board) == O:
        temp = math.inf
        for action in actions(board):
            max_val = max_node(result(board, action))

            if max_val < temp:
                temp = max_val
                best_action = action

    return best_action


def min_node(board):

    if terminal(board):
        return utility(board)

    max_val = math.inf
    for action in actions(board):
        max_val = min(max_val, max_node(result(board, action)))
    return max_val


def max_node(board):

    if terminal(board):
        return utility(board)

    min_val = -math.inf
    for action in actions(board):
        min_val = max(min_val, min_node(result(board, action)))
    return min_val

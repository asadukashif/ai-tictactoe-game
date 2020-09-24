"""
Tic Tac Toe Player
"""

import math
from itertools import permutations

X = "X"
O = "O"
EMPTY = None
INFINITY = math.inf
default_turn = X
current_turn = X


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
    X_count = 0
    O_count = 0
    game_over = True

    for row in range(3):
        for col in range(3):
            cell = board[row][col]
            if cell == X:
                X_count += 1
            elif cell == O:
                O_count += 1
            elif cell == EMPTY:
                game_over = False

    if X_count == O_count:
        return default_turn
    if X_count > O_count:
        return O
    if X_count < O_count:
        return X

    if game_over:
        return "Game Over"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for row in range(3):
        for col in range(3):
            cell = board[row][col]
            if cell == EMPTY:
                action = (row, col)
                possible_actions.add(action)

    return possible_actions


def deep_copy(board):
    """
    Returns a deep copy of the current board
    """
    board_copy = [[], [], []]
    for i in range(3):
        for j in range(3):
            board_copy[i].append(board[i][j])

    return board_copy


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action is None:
        return board

    new_board = deep_copy(board)
    player_turn = player(board)

    row, col = action

    if board[row][col] == EMPTY:
        new_board[row][col] = player_turn
    else:
        raise Exception(f"This place ({row},{col}) is not empty")

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # For complete row check
    for i in range(3):
        X_three_in_row = True
        O_three_in_row = True
        for j in range(3):
            X_three_in_row &= (board[i][j] == X)
            O_three_in_row &= (board[i][j] == O)
        if X_three_in_row:
            return X
        if O_three_in_row:
            return O

    # For complete column check
    for i in range(3):
        X_three_in_row = True
        O_three_in_row = True
        for j in range(3):
            X_three_in_row &= (board[j][i] == X)
            O_three_in_row &= (board[j][i] == O)
        if X_three_in_row:
            return X
        if O_three_in_row:
            return O

    # For diagnals
    # Principal Diagnal
    X_three_in_row = True
    O_three_in_row = True
    for i in range(3):
        for j in range(3):
            if i == j:
                X_three_in_row &= (board[j][i] == X)
                O_three_in_row &= (board[j][i] == O)
    if X_three_in_row:
        return X
    if O_three_in_row:
        return O
    # Secondary Diagnal
    X_three_in_row = True
    O_three_in_row = True
    for i in range(3):
        for j in range(3):
            if not (i == 0 and j == 0):
                if (abs(i + j) - 2 == 0):
                    X_three_in_row &= (board[i][j] == X)
                    O_three_in_row &= (board[i][j] == O)

    if X_three_in_row:
        return X
    if O_three_in_row:
        return O

    return None


def completely_filled(board):
    """
    Return True if the board is completely filled else return False
    """
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False

    return True


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    board_status = winner(board)
    if board_status is not None:
        return True
    elif board_status is None:
        if completely_filled(board):
            return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winning_player = winner(board)
    if winning_player == X:
        return 1
    if winning_player == O:
        return -1
    if winning_player == None:
        return 0


def solve_board(board_original, initial_aciton):
    """
    Returns the depth and utility of the board after performing all the actions on the board
    """
    board = deep_copy(board_original)
    board = result(board, initial_aciton)

    possible_actions = actions(board)

    for action in possible_actions:
        if not terminal(board):
            temp_board = deep_copy(board)
            action = minimax(temp_board)
            board = result(board, action)

    return utility(board)


def minimax(board_original):
    """
    Returns the optimal move for the AI
    """
    board = deep_copy(board_original)
    possible_actions = actions(board)
    if len(possible_actions) == 9:
        return (0, 0)
    moves_t = []
    scores_t = []

    for action in possible_actions:
        score = solve_board(board, action)
        move = {'action': action, 'score': score}
        moves_t.append(move)
        scores_t.append(score)

    # X -> Maximizing
    # O -> Minimizing
    turn = player(board_original)
    best_score = min(scores_t) if turn == O else max(scores_t)
    best_action = None

    for move in moves_t:
        if move['score'] == best_score:
            best_action = move['action']

    return best_action

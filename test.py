from tictactoe import winner, terminal, player, initial_state, minimax, result, utility, deep_copy, actions

X = 'X'
O = 'O'
EMPTY = None

board = [[O,    X,         O],
         [X,    EMPTY,     X],
         [X,    EMPTY,     O]]

print(minimax(board))

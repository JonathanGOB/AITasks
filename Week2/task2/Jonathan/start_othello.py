"""

Othello is a turn-based two-player strategy board game.

-----------------------------------------------------------------------------
Board representation

We represent the board as a 100-element list, which includes each square on
the board as well as the outside edge. Each consecutive sublist of ten
elements represents a single row, and each list element stores a piece. 
An initial board contains four pieces in the center:

    ? ? ? ? ? ? ? ? ? ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . o @ . . . ?
    ? . . . @ o . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? ? ? ? ? ? ? ? ? ?

This representation has two useful properties:

1. Square (m,n) can be accessed as `board[mn]`. This is because size of square is 10x10,
   and mn means m*10 + n. This avoids conversion between square locations and list indexes.
2. Operations involving bounds checking are slightly simpler.
"""

# The outside edge is marked ?, empty squares are ., black is @, and white is o.
# The black and white pieces represent the two players.
import os
import random
import time

EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11

# 8 directions; note UP_LEFT = -11, we can repeat this from row to row
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

weights = [64, -8, 8, 8, 8, 8, -8, 64,
           -8, -8, 0, 0, 0, 0, -8, -8,
           8, 0, 0, 0, 0, 0, 0, 8,
           8, 0, 0, 0, 0, 0, 0, 8,
           8, 0, 0, 0, 0, 0, 0, 8,
           8, 0, 0, 0, 0, 0, 0, 8,
           -8, -8, 0, 0, 0, 0, -8, -8,
           64, -8, 8, 8, 8, 8, -8, 64]


def squares():
    # list all the valid squares on the board.
    # returns a list [11, 12, 13, 14, 15, 16, 17, 18, 21, ...]; e.g. 19,20,21 are invalid
    # 11 means first row, first col, because the board size is 10x10
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]


def initial_board():
    # create a new board with the initial black and white positions filled
    # returns a list ['?', '?', '?', ..., '?', '?', '?', '.', '.', '.', ...]
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    # the middle four squares should hold the initial piece positions.
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    weight_matrix = [OUTER] * 100
    weightsiter = iter(weights)
    for i in squares():
        weight_matrix[i] = next(weightsiter)
    return board, weight_matrix


def print_board(board):
    # get a string representation of the board
    # heading '  1 2 3 4 5 6 7 8\n'
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    # begin,end = 11,19 21,29 31,39 ..
    for row in range(1, 9):
        begin, end = 10 * row + 1, 10 * row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    return rep


# -----------------------------------------------------------------------------
# Playing the game

# We need functions to get moves from players, check to make sure that the moves
# are legal, apply the moves to the board, and detect when the game is over.

# Checking moves. # A move must be both valid and legal: it must refer to a real square,
# and it must form a bracket with another piece of the same color with pieces of the
# opposite color in between.

def is_valid(move):
    # is move a square on the board?
    # move must be an int, and must refer to a real square
    return isinstance(move, int) and move in squares()


def opponent(player):
    # get player's opponent piece
    return BLACK if player is WHITE else WHITE


def find_bracket(square, player, board, direction):
    # find and return the square that forms a bracket with `square` for `player` in the given
    # `direction`
    # returns None if no such square exists
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    # if last square board[bracket] not in (EMPTY, OUTER, opp) then it is player
    return None if board[bracket] in (OUTER, EMPTY) else bracket


def is_legal(move, player, board):
    # is this a legal move for the player?
    # move must be an empty square and there has to be is an occupied line in some direction
    # any(iterable) : Return True if any element of the iterable is true
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(hasbracket(x) for x in DIRECTIONS)


# Making moves
# When the player makes a move, we need to update the board and flip all the
# bracketed pieces.

def make_move(move, player, board):
    # update the board to reflect the move by the specified player
    # assuming now that the move is valid
    board[move] = player
    # look for a bracket in any direction
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board


def make_flips(move, player, board, direction):
    # flip pieces in the given direction as a result of the move by player
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    # found a bracket in this direction
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction


# Monitoring players

# define an exception
class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board

    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)


def legal_moves(player, board):
    # get a list of all legal moves for player
    # legals means : move must be an empty square and there has to be is an occupied line in some direction
    return [sq for sq in squares() if is_legal(sq, player, board)]


def any_legal_move(player, board):
    # can player make any moves?
    return any(is_legal(sq, player, board) for sq in squares())


# Putting it all together

# Each round consists of:
# - Get a move from the current player.
# - Apply it to the board.
# - Switch players. If the game is over, get the final score.

def play(black_strategy, white_strategy):
    # play a game of Othello and return the final board and score
    global weights
    board, weights = initial_board()
    print(print_board(board))
    not_finished = True
    current_player = WHITE
    done_counter = 0
    while not_finished:
        if next_player(board, current_player):
            current_player = next_player(board, current_player)
            get_move(black_strategy if current_player == BLACK else white_strategy, current_player, board)
            os.system('cls')
            print(print_board(board))
            done_counter = 0
        else:
            current_player = next_player(board, current_player)
            done_counter += 1
        if done_counter == 2:
            not_finished = False
    print("score WHITE {} points".format(result(WHITE, board)))
    print("score BLACK {} points".format(result(BLACK, board)))
    print("MAX TIME {} DEPTH {}".format(GLOBAL_TIME["TIME"], GLOBAL_DEPTH))


def next_player(board, prev_player):
    # which player should move next?  Returns None if no legal moves exist
    antogonist = opponent(prev_player)
    return antogonist if any_legal_move(antogonist, board) else None


GLOBAL_TIME = {"TIME": 0}


def get_move(strategy, player, board):
    # call strategy(player, board) to get a move
    t0 = time.process_time()
    move = strategy(GLOBAL_DEPTH, player, board, 1)
    t1 = time.process_time()
    if GLOBAL_TIME["TIME"] < t1 - t0:
        if strategy.__name__ == "negamaxABpruning":
            GLOBAL_TIME["TIME"] = t1 - t0
            print(strategy.__name__, "time  {} ".format(t1 - t0))
    make_move(move, player, board)
    return True


def result(player, board):
    # compute player's score (number of player's pieces minus opponent's)
    total_score = 0
    for e in squares():
        if board[e] == player:
            total_score += 1
    return total_score


def score(player, board):
    # compute player's score (number of player's pieces minus opponent's)
    total_score = 0
    for e in squares():
        if board[e] == player:
            total_score += 1 * weights[e] + 1
    return total_score


GLOBAL_DEPTH = 7


def negamaxABpruning(depth, player, board, current, A=-1000, B=1000):
    optimal = None
    move = None
    if depth == 0 or (not any_legal_move(next_player(board, player), board) and any_legal_move(player, board)):
        return current * score(player, board)
    if any_legal_move(player if current == 1 else next_player(board, player), board):
        for e in legal_moves(player if current == 1 else next_player(board, player), board):
            new_board = board[:]
            make_move(e, player if current == 1 else next_player(new_board, player), new_board)
            heuristic = -negamaxABpruning(depth - 1, player, new_board, -current, -A, -B)
            A = max(A, heuristic)
            if optimal:
                if heuristic > optimal:
                    move = e
                    optimal = heuristic
            if not optimal:
                move = e
                optimal = heuristic
            if A >= B:
                break
    else:
        new_board = board[:]
        heuristic = -negamaxABpruning(depth - 1, player, new_board, -current)
        A = max(A, heuristic)
        if optimal:
            if heuristic > optimal:
                optimal = heuristic
        if not optimal:
            optimal = heuristic

    if GLOBAL_DEPTH == depth:
        return move
    return optimal


def negamax(depth, player, board, current, A = None, B = None):
    optimal = None
    move = None
    if depth == 0 or (not any_legal_move(next_player(board, player), board) and any_legal_move(player, board)):
        return current * score(player, board)
    if any_legal_move(player if current == 1 else next_player(board, player), board):
        for e in legal_moves(player if current == 1 else next_player(board, player), board):
            new_board = board[:]
            make_move(e, player if current == 1 else next_player(new_board, player), new_board)
            heuristic = -negamax(depth - 1, player, new_board, -current)
            if optimal:
                if heuristic > optimal:
                    move = e
                    optimal = heuristic
            if not optimal:
                move = e
                optimal = heuristic
    else:
        new_board = board[:]
        heuristic = -negamax(depth - 1, player, new_board, -current)
        if optimal:
            if heuristic > optimal:
                optimal = heuristic
        if not optimal:
            optimal = heuristic

    if GLOBAL_DEPTH == depth:
        return move
    return optimal


def random_move(depth, player, board, current):
    number = random.choice(legal_moves(player, board))
    return number


def random_move1(depth, player, board, current, A=None, B=None):
    number = random.choice(legal_moves(player, board))
    return number


# Play strategies
if __name__ == "__main__":
    play(negamaxABpruning, negamax)

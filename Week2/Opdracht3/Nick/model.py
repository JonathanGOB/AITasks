import random
import itertools
import math
import copy
import numpy

MAX_DEPTH = 6


def merge_left(b):
    # merge the board left
    # this is the function that is reused in the other merges
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]    
    def merge(row, acc):
        # recursive helper for merge_left

        # if len row == 0, return accumulator
        if not row:
            return acc

        # x = first element
        x = row[0]
        # if len(row) == 1, add element to accumulator
        if len(row) == 1:
            return acc + [x]

        # if len(row) >= 2
        if x == row[1]:
            # add row[0] + row[1] to accumulator, continue with row[2:]
            return merge(row[2:], acc + [2 * x])
        else:
            # add row[0] to accumulator, continue with row[1:]
            return merge(row[1:], acc + [x])

    new_b = []
    for row in b:
        # merge row, skip the [0]'s
        merged = merge([x for x in row if x != 0], [])
        # add [0]'s to the right if necessary
        merged = merged + [0] * (len(row) - len(merged))
        new_b.append(merged)
    # return [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    return new_b


def merge_right(b):
    # merge the board right
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    def reverse(x):
        return list(reversed(x))

    # rev = [[4, 4, 2, 0], [8, 4, 2, 0], [4, 0, 0, 0], [2, 2, 2, 2]]
    rev = [reverse(x) for x in b]
    # ml = [[8, 2, 0, 0], [8, 4, 2, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    ml = merge_left(rev)
    # return [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    return [reverse(x) for x in ml]


def merge_up(b):
    # merge the board upward
    # note that zip(*b) is the transpose of b
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[2, 0, 0, 0], [4, 2, 0, 0], [8, 2, 0, 0], [4, 8, 4, 2]]
    trans = merge_left(zip(*b))
    # return [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    return [list(x) for x in zip(*trans)]


def merge_down(b):
    # merge the board downward
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[0, 0, 0, 2], [0, 0, 2, 4], [0, 0, 8, 2], [4, 8, 4, 2]]
    trans = merge_right(zip(*b))
    # return [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    return [list(x) for x in zip(*trans)]


# location: after functions
MERGE_FUNCTIONS = {
    'left': merge_left,
    'right': merge_right,
    'up': merge_up,
    'down': merge_down
}


def move_exists(b):
    # check whether or not a move exists on the board
    # b = [[1, 2, 3, 4], [5, 6, 7, 8]]
    # move_exists(b) return False
    def inner(b):
        for row in b:
            for x, y in zip(row[:-1], row[1:]):
                # tuples (1, 2),(2, 3),(3, 4),(5, 6),(6, 7),(7, 8)
                if x == y or x == 0 or y == 0:
                    return True
        return False

    if inner(b) or inner(zip(*b)):
        return True
    else:
        return False


def start():
    # make initial board
    b = [[0] * 4 for _ in range(4)]
    add_two_four(b)
    add_two_four(b)
    return b


def play_move(b, direction):
    # get merge function an apply it to board
    b = MERGE_FUNCTIONS[direction](b)
    add_two_four(b)
    return b


def add_two_four(b):
    # add a random tile to the board at open position.
    # chance of placing a 2 is 90%; chance of 4 is 10%
    rows, cols = list(range(4)), list(range(4))
    random.shuffle(rows)
    random.shuffle(cols)
    distribution = [2] * 9 + [4]
    for i, j in itertools.product(rows, rows):
        if b[i][j] == 0:
            b[i][j] = random.sample(distribution, 1)[0]
            return (b)
        else:
            continue


def game_state(b):
    for i in range(4):
        for j in range(4):
            if b[i][j] >= 2048:
                return 'win'
    return 'lose'


def test():
    b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    assert merge_left(b) == [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    assert merge_right(b) == [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    assert merge_up(b) == [(2, 4, 8, 4), (0, 2, 2, 8), (0, 0, 0, 4), (0, 0, 0, 2)]
    assert merge_down(b) == [(0, 0, 0, 4), (0, 0, 0, 8), (0, 2, 8, 4), (2, 4, 2, 2)]
    assert move_exists(b) == True
    b = [[2, 8, 4, 0], [16, 0, 0, 0], [2, 0, 2, 0], [2, 0, 0, 0]]
    assert (merge_left(b)) == [[2, 8, 4, 0], [16, 0, 0, 0], [4, 0, 0, 0], [2, 0, 0, 0]]
    assert (merge_right(b)) == [[0, 2, 8, 4], [0, 0, 0, 16], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert (merge_up(b)) == [(2, 8, 4, 0), (16, 0, 2, 0), (4, 0, 0, 0), (0, 0, 0, 0)]
    assert (merge_down(b)) == [(0, 0, 0, 0), (2, 0, 0, 0), (16, 0, 4, 0), (4, 8, 2, 0)]
    assert (move_exists(b)) == True
    b = [[0, 7, 0, 0], [0, 0, 7, 7], [0, 0, 0, 7], [0, 7, 0, 0]]
    # g = Game() TODO find out what he means with this
    # for i in range(11):
    #     g.add_two_four(b)


def get_random_move():
    return random.choice(list(MERGE_FUNCTIONS.keys()))


# direction = model.value(self.board) First call
# expected value is 0.1 * 4 + 0.9 * 2
# search and evaluation function

def get_move(board):
    h_move = ""
    h_score = -1

    for direction in MERGE_FUNCTIONS.keys():
        new_board = copy.deepcopy(board)
        next_step = play_move(new_board, direction)
        if new_board == next_step:  # Check if the direction doesn't change the board, so skip
            continue
        score = value(board, MAX_DEPTH, "MAX")
        if score > h_score:
            h_score = score
            h_move = direction
    return h_move


def value(board, depth, player):
    if depth == 0:
        if not move_exists(board):
            return -100000
        return calculate_heuristic(board)
    if player == "MAX":
        return max_value(board, depth)
    else:
        return exp_value(board, depth)


def max_value(board, depth):
    v = -math.inf
    for direction in MERGE_FUNCTIONS.keys():
        new_board = play_move(board, direction)
        v = max(v, value(new_board, depth-1, "EXP"))
    return v


# def exp_value(board, depth):   TODO Not correct
#     sum = 0
#     num = 0
#     for cell in get_empty_cells(board):
#         new_board = copy.deepcopy(board)
#         x, y = cell
#         new_board[x][y] = 2
#         sum += (0.9 * value(new_board, depth-1, "MAX"))
#         new_board[x][y] = 4
#         sum += (0.1 * value(new_board, depth-1, "MAX"))
#         num += 1
#     if num == 0:
#         return value(board, depth-1, "MAX")
#     return sum/num
#
#
# def get_empty_cells(board):
#     empty_cells = []
#     count_x = -1
#     for x in board:
#         count_x += 1
#         count_y = -1
#         for y in x:
#             count_y += 1
#             if y == 0:
#                 empty_cells.append([count_x, count_y])
#     return empty_cells
def exp_value(board, depth):
    total = 0
    num = 0
    for _ in range(get_empty_cells(board)):
        new_board = add_two_four(board)
        total += value(new_board, depth-1, "MAX")
        num += 1
    if num == 0:
        return value(board, depth-1, "MAX")
    return total/num


def get_empty_cells(board):
    empty_cells = 0
    for x in board:
        for y in x:
            if y == 0:
                empty_cells += 1
    return empty_cells


def calculate_heuristic(board):
    heuristic = 0
    heuristic += left_top_heuristic(board)
    heuristic -= cluster_heuristics(board)
    heuristic += monotonic_heuristics(board)
    return heuristic


def left_top_heuristic(b):  # Give higher score to top left cells
    board = numpy.array(b)
    h = numpy.array([[30, 15, 5, 3],
                     [15, 5, 3, 1],
                     [5, 3, 1, 0],
                     [3, 1, 0, 0]])
    return numpy.sum(h*board)


def cluster_heuristics(board):  # Give a penalty to cells with a different value next to each other
    penalty = 0
    for x in range(4):
        for y in range(4):
            if y >= 0:  # left
                penalty = penalty + abs(board[x][y] - board[x][y-1])
            if x >= 0:  # top
                penalty = penalty + abs(board[x][y] - board[x][y-1])
            if y < 3:  # right
                penalty = penalty + abs(board[x][y] - board[x][y+1])
            if x < 3:  # bottom
                penalty = penalty + abs(board[x][y] - board[x+1][y])
    return penalty


def monotonic_heuristics(board):
    cells = numpy.array(board)
    size = 4
    cells[cells < 1] = 0.1
    score1 = cells[1:size, 3]/cells[:size-1, 3]
    score2 = cells[3, 1:size]/cells[3, :size-1]
    score = numpy.sum(score1[score1 == 2])
    score += numpy.sum(score2[score2 == 2])
    return score * 20


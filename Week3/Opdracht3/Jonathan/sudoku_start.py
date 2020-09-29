import os
import time
import copy

# helper function
from collections import namedtuple


def cross(A, B):
    # cross product of chars in string A and chars in string B
    return [a + b for a in A for b in B]


#   1 2 3 4 .. 9
# A
# B
# C
# D
# ..
# I

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
cells = cross(rows, cols)  # for 3x3 81 cells A1..9, B1..9, C1..9, ...

# unit = a row, a column, a box; list of all units
unit_list = ([cross(r, cols) for r in rows] +  # 9 rows
             [cross(rows, c) for c in cols] +  # 9 cols
             [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])  # 9 units
# peers is a dict {cell : list of peers}
# every cell c has 20 peers p (i.e. cells that share a row, col, box)
# units['A1'] is a list of lists, and sum(units['A1'],[]) flattens this list
units = dict((s, [u for u in unit_list if s in u]) for s in cells)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in cells)


def display(grid):
    # grid is a dict of {cell: string}, e.g. grid['A1'] = '1234'
    print()
    for r in rows:
        for c in cols:
            v = grid[r + c]
            # avoid the '123456789'
            if v == '123456789':
                v = '.'
            print(''.join(v), end=' ')
            if c == '3' or c == '6': print('|', end='')
        print()
        if r == 'C' or r == 'F':
            print('-------------------')
    print()


def parse_string_to_dict(grid_string):
    # grid_string is a string like '4.....8.5.3..........7......2.....6....   '
    # convert grid_string into a dict of {cell: chars}
    char_list1 = [c for c in grid_string if c in digits or c == '.']
    # char_list1 = ['8', '5', '.', '.', '.', '2', '4', ...  ]
    assert len(char_list1) == 81

    # replace '.' with '1234567'
    char_list2 = [s.replace('.', '123456789') for s in char_list1]

    # grid {'A1': '8', 'A2': '5', 'A3': '123456789',  }
    return dict(zip(cells, char_list2))


def parse_dict_to_string(dict):
    return "".join(e if e != digits else '.' for e in dict.values())


def no_conflict(grid, c, v):
    # check if assignment is possible: value v not a value of a peer
    for p in peers[c]:
        if grid[p] == v:
            return False  # conflict
    return True


# def solve(grid):
#     # backtracking search a solution (DFS)
#     # your code here
#     for key, value in grid.items():
#         if value == digits:
#             for i in range(1, 10):
#                 if no_conflict(grid, key, str(i)):
#                     grid[key] = str(i)
#                     solve(grid)
#                     grid[key] = digits
#             return
#     print('\nAnswer')
#     print(display(grid))
#     print(parse_dict_to_string(grid))

def get_next_empty_spot(node):
    for key, value in node.items():
        if value == digits:
            return key


def filter_moves(key, node):
    return [str(e) for e in range(1, 10) if no_conflict(node, key, str(e))]


def move_actions(node):
    key = get_next_empty_spot(node)
    options = filter_moves(key, node)
    for option in options:
        new_node = node.copy()
        new_node[key] = option
        yield new_node


def solve(grid):
    # backtracking search a solution (DFS) without arc
    # your code here

    # visited and stack
    visited, stack = set(), [grid]

    # while there is a stack
    while stack:
        node = stack.pop()

        # if all places filled
        if all(len(value) == 1 for value in node.values()):
            print(f"found {node}")
            return node

        # str for dictionary for visited
        visitor = hash(frozenset(node.items()))

        if visitor not in visited:
            visited.add(visitor)
            stack.extend([move_state for move_state in move_actions(node)])


def solve_with_arc(grid):
    # backtracking search a solution (DFS) and ARC-consistency
    # your code here

    # visited and stack
    visited, stack = set(), [grid]

    # while there is a stack
    while stack:
        node = stack.pop()

        # if all places filled
        if all(len(value) == 1 for value in node.values()):
            print(f"found {node}")
            return node

        # str for dictionary for visited
        visitor = hash(frozenset(node.items()))

        if visitor not in visited:
            visited.add(visitor)
            key, text = min(node.items(), key=lambda x: len(x[1]) if len(x[1]) > 1 else float('inf'))
            for number in text:
                new_grid = node.copy()
                new_grid[key] = number
                if make_arc_consistent_recursive(new_grid, key, number):
                    stack.append(new_grid)


def make_arc_consistent_iterative(grid, key, value):
    CSP = namedtuple("pair", ["key", "value"])
    stack = [CSP(key, value)]
    conflict = False
    while stack:
        changed = False
        node = stack.pop()
        for r in peers[node.key]:
            if node.value in grid[r]:
                if len(grid[r]) <= 1:
                    conflict = True
                    break
                else:
                    grid[r] = grid[r].replace(node.value, "")
                    changed = True
        if conflict:
            return False
        if changed:
            list_cells = [e for e in peers[node.key] if len(grid[e]) == 1 and e != node.key]
            for cell in list_cells:
                stack.append(CSP(cell, grid[cell]))
    return True


def make_arc_consistent_recursive(grid, key, value):
    changed = False
    for r in peers[key]:
        if value in grid[r]:
            if len(grid[r]) <= 1:
                return False
            else:
                grid[r] = grid[r].replace(value, "")
                changed = True
    if changed:
        list_cells = [e for e in peers[key] if len(grid[e]) == 1 and e != key]
        for cell in list_cells:
            if not make_arc_consistent_recursive(grid, cell, grid[cell]):
                return False
    return True


# minimum nr of clues for a unique solution is 17
slist = [None for x in range(20)]
slist[0] = '.56.1.3....16....589...7..4.8.1.45..2.......1..42.5.9.1..4...899....16....3.6.41.'
slist[1] = '.6.2.58...1....7..9...7..4..73.4..5....5..2.8.5.6.3....9.73....1.......93......2.'
slist[2] = '.....9.73.2.....569..16.2.........3.....1.56..9....7...6.34....7.3.2....5..6...1.'
slist[3] = '..1.3....5.917....8....57....3.1.....8..6.59..2.9..8.........2......6...315.9...8'
slist[4] = '....6.8748.....6.3.....5.....3.4.2..5.2........72...35.....3..........69....96487'
slist[5] = '.94....5..5...7.6.........71.2.6.........2.19.6...84..98.......51..9..78......5..'
slist[6] = '.5...98..7...6..21..2...6..............4.598.461....5.54.....9.1....87...2..5....'
slist[7] = '...17.69..4....5.........14.....1.....3.5716..9.....353.54.9....6.3....8..4......'
slist[8] = '..6.4.5.......2.3.23.5..8765.3.........8.1.6.......7.1........5.6..3......76...8.'
slist[9] = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
slist[10] = '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'
slist[11] = '...5....2...3..85997...83..53...9...19.73...4...84...1.471..6...5...41...1...6247'
slist[12] = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
slist[13] = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
slist[14] = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
slist[15] = '6..3.2....5.....1..........7.26............543.........8.15........4.2........7..'
slist[16] = '.6.5.1.9.1...9..539....7....4.8...7.......5.8.817.5.3.....5.2............76..8...'
slist[17] = '..5...987.4..5...1..7......2...48....9.1.....6..2.....3..6..2.......9.7.......5..'
slist[18] = '3.6.7...........518.........1.4.5...7.....6.....2......2.....4.....8.3.....5.....'
slist[19] = '1.....3.8.7.4..............2.3.1...........958.........5.6...7.....8.2...4.......'


def test():
    # a set of tests that must pass
    assert len(cells) == 81
    assert len(unit_list) == 27
    assert all(len(units[s]) == 3 for s in cells)
    assert all(len(peers[s]) == 20 for s in cells)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print('All tests pass.')


for i, sudo in enumerate(slist):
    print('*** sudoku {0} ***'.format(i))
    d = parse_string_to_dict(sudo)
    print(display(d))
    print(d)
    start_time = time.time()
    found = solve_with_arc(d)
    end_time = time.time()
    hours, rem = divmod(end_time - start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print(display(found))
    print("duration [hh:mm:ss.ddd]: {:0>2}:{:0>2}:{:06.3f}".format(int(hours), int(minutes), seconds))
    print()

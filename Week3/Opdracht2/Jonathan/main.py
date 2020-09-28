import itertools

BOARD = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None}
VALUES = ["A", "A", "K", "K", "Q", "Q", "J", "J"]


def generate_permutations():
    for values in list(itertools.permutations(VALUES)):
        temp_board = BOARD.copy()
        for index in range(len(values)):
            temp_board[index] = values[index]  # Generate a board option
        yield temp_board


NEIGHBORS = [(0, 3), (1, 2), (6, 5), (7, 5), (4, 2, 5), (2, 1, 3, 4), (3, 0, 2, 5), (5, 3, 6, 7, 4)]


def check_boards():
    valid_boards = []
    visited_boards = []
    for board in generate_permutations():
        A_PASS = 0
        H_PASS = 0
        Q_PASS = 0
        AQ_PASS = True
        SIM_PASS = True
        visited = []
        for key, value in board.items():
            for e in NEIGHBORS:
                if e[0] == key:
                    for n in e[1:]:
                        if value == "A" and board[n] == "K":
                            if key not in visited:
                                visited.append(key)
                                A_PASS += 1
                        if value == "K" and board[n] == "Q":
                            if key not in visited:
                                visited.append(key)
                                H_PASS += 1
                        if value == "Q" and board[n] == "J":
                            if key not in visited:
                                visited.append(key)
                                Q_PASS += 1
                        if value == "A" and board[n] == "Q":
                            AQ_PASS = False
                        if value == board[n]:
                            SIM_PASS = False
        if A_PASS == 2 and H_PASS == 2 and Q_PASS == 2 and AQ_PASS and SIM_PASS:
            if hash(frozenset(board.items())) not in visited_boards:
                visited_boards.append(hash(frozenset(board.items())))
                valid_boards.append(board)
    return valid_boards

def no_conflict(value, key, board):
    PASS = False
    for s in NEIGHBORS:
        if s[0] == key:
            check_list = s[1:]
            for n in range(len(check_list)):
                if board[key] == "A" and board[check_list[n]] == "K":
                    PASS = True
                if board[key] == "K" and board[check_list[n]] == "Q":
                    PASS = True
                if board[key] == "Q" and board[check_list[n]] == "J":
                    PASS = True
                if n == len(check_list) - 1 and PASS == False:
                    PASS = True
                if board[key] == "A" and board[check_list[n]] == "Q":
                    PASS = False
                if value == board[check_list[n]]:
                    PASS = False
    return PASS

def dfs_card_game(board, solutions, visited, USEABLE):
    if all(value != None for value in board.values()):
        solutions.append(board)
        return solutions

    for key, value in board.items():
        if value is None:
            for e in USEABLE:
                temp_board = board.copy()
                if no_conflict(e, key, temp_board):
                    temp_board[key] = e
                    visitor = hash(frozenset(temp_board.items()))
                    if visitor not in visited:
                        visited.append(visitor)
                        used_copy = USEABLE[:]
                        del used_copy[used_copy.index(e)]
                        dfs_card_game(temp_board, solutions, visited, used_copy)
    return solutions


def print_result(boards):
    print("SOLVED {}".format(len(boards)))
    for board in boards:
        print_board(board)


def print_board(board):
    print(". . {} .".format(board[0]))
    print("{} {} {} .".format(board[1], board[2], board[3]))
    print(". {} {} {}".format(board[4], board[5], board[6]))
    print(". . {} .".format(board[7]))
    print()


print_result(dfs_card_game(BOARD, [], [], VALUES))

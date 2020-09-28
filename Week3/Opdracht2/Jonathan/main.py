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


def no_conflict(value, key, board, usable):
    PASS = False
    for s in NEIGHBORS:
        if s[0] == key:
            check_list = s[1:]
            for n in range(len(check_list)):
                if value == "A" and board[check_list[n]] == "K" or board[
                    check_list[n]] is None and "K" in usable and usable.count("A") > usable.count("K"):
                    PASS = True
                if value == "K" and board[check_list[n]] == "Q" or board[
                    check_list[n]] is None and "Q" in usable and usable.count("K") > usable.count("Q"):
                    PASS = True
                if value == "Q" and board[check_list[n]] == "J" or board[
                    check_list[n]] is None and "J" in usable and usable.count("Q") > usable.count("J"):
                    PASS = True
                if value == "A" and board[check_list[n]] == "Q":
                    return False
                if value == board[check_list[n]]:
                    return False
    return PASS


def check_board(board):
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
        return True
    else:
        return False


ITERATION = {"iteration": 0}


def dfs_card_game(board, solutions, visited, USEABLE):
    if all(value is not None for value in board.values()) and check_board(board):
        if len(solutions) == 0:
            print_board(board)
            print(ITERATION["iteration"])
        solutions.append(board)
        return solutions

    for key, value in board.items():
        if value is None:
            for e in range(len(USEABLE)):
                temp_board = board.copy()
                used_copy = USEABLE[:]
                del used_copy[e]
                if no_conflict(USEABLE[e], key, board, used_copy):
                    temp_board[key] = USEABLE[e]
                    if temp_board not in visited:
                        visited.append(temp_board)
                        ITERATION["iteration"] += 1
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


print_result(check_boards())
print_result(dfs_card_game(BOARD, [], [], VALUES))

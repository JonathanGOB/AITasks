import itertools

# Questions
# 1a 40320 calculate by 8!

# Rules
# 1. Each A has a H
# 2. Each H has a V
# 3. Each V has a B
# 4. Each A doesn't border a V
# 5. Same suit can't border each other

BOARD = {
    0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None
}

VALUES = ["A", "A", "K", "K", "Q", "Q", "J", "J"]
ONE_NEIGHBOR = [(0, 3), (1, 2), (6, 5), (7, 5)]
TWO_NEIGHBORS = [(4, 2, 5)]
THREE_NEIGHBORS = [(2, 1, 3, 4), (3, 0, 2, 5)]
FOUR_NEIGHBORS = [(5, 3, 6, 7, 4)]


def print_result(permutations):
    for pos, value in BOARD.items():
        print(str(pos) + "=" + str(value), end=" ")
    print("\nAmount of permutations: " + str(permutations))


def generate_options():
    permutations = 0
    for values in list(itertools.permutations(VALUES)):
        permutations += 1
        for index in range(8):
            BOARD[index] = values[index]  # Generate a board option
        if check_correct():
            return print_result(permutations)


def check_correct():
    # One neighbor tests
    for x in ONE_NEIGHBOR:
        if BOARD[x[0]] == "A":
            if BOARD[x[1]] != "K":  # Rule 1
                return False
        if BOARD[x[0]] == "K":
            if BOARD[x[1]] != "Q":  # Rule 2
                return False
        if BOARD[x[0]] == "Q":
            if BOARD[x[1]] != "J":  # Rule 3
                return False
        if BOARD[x[0]] == "J":
            if BOARD[x[1]] == "J":  # Rule 5
                return False
    # Two neighbors tests
    for x in TWO_NEIGHBORS:
        if BOARD[x[0]] == "A":
            if BOARD[x[1]] != "K" and BOARD[x[2]] != "K":  # Rule 1
                return False
            if BOARD[x[1]] == "Q" or BOARD[x[2]] == "Q":  # Rule 4
                return False
            if BOARD[x[1]] == "A" or BOARD[x[2]] == "A":  # Rule 5
                return False
        if BOARD[x[0]] == "K":
            if BOARD[x[1]] != "Q" and BOARD[x[2]] != "Q":  # Rule 2
                return False
            if BOARD[x[1]] == "K" or BOARD[x[2]] == "K":  # Rule 5
                return False
        if BOARD[x[0]] == "Q":
            if BOARD[x[1]] != "J" and BOARD[x[2]] != "J":  # Rule 3
                return False
            if BOARD[x[1]] == "Q" or BOARD[x[2]] == "Q":  # Rule 5
                return False
        if BOARD[x[0]] == "J":
            if BOARD[x[1]] == "J" or BOARD[x[2]] == "J":  # Rule 5
                return False
    # Three neighbors tests
    for x in THREE_NEIGHBORS:
        if BOARD[x[0]] == "A":
            if BOARD[x[1]] != "K" and BOARD[x[2]] != "K" and BOARD[x[3]] != "K":  # Rule 1
                return False
            if BOARD[x[1]] == "Q" or BOARD[x[2]] == "Q" or BOARD[x[3]] == "Q":  # Rule 4
                return False
            if BOARD[x[1]] == "A" or BOARD[x[2]] == "A" or BOARD[x[3]] == "A":  # Rule 5
                return False
        if BOARD[x[0]] == "K":
            if BOARD[x[1]] != "Q" and BOARD[x[2]] != "Q" and BOARD[x[3]] != "Q":  # Rule 2
                return False
            if BOARD[x[1]] == "K" or BOARD[x[2]] == "K" or BOARD[x[3]] == "K":  # Rule 5
                return False
        if BOARD[x[0]] == "Q":
            if BOARD[x[1]] != "J" and BOARD[x[2]] != "J" and BOARD[x[3]] != "J":  # Rule 3
                return False
            if BOARD[x[1]] == "Q" or BOARD[x[2]] == "Q" or BOARD[x[3]] == "Q":  # Rule 5
                return False
        if BOARD[x[0]] == "J":
            if BOARD[x[1]] == "J" or BOARD[x[2]] == "J" or BOARD[x[3]] == "J":  # Rule 5
                return False
    # Four neighbors tests
    for x in FOUR_NEIGHBORS:
        if BOARD[x[0]] == "A":
            if BOARD[x[1]] != "K" and BOARD[x[2]] != "K" and BOARD[x[3]] != "K" and BOARD[x[4]] != "K":  # Rule 1
                return False
            if BOARD[x[1]] == "Q" or BOARD[x[2]] == "Q" or BOARD[x[3]] == "Q" or BOARD[x[4]] == "Q":  # Rule 4
                return False
            if BOARD[x[1]] == "A" or BOARD[x[2]] == "A" or BOARD[x[3]] == "A" or BOARD[x[4]] == "A":  # Rule 5
                return False
        if BOARD[x[0]] == "K":
            if BOARD[x[1]] != "Q" and BOARD[x[2]] != "Q" and BOARD[x[3]] != "Q" and BOARD[x[4]] != "Q":  # Rule 2
                return False
            if BOARD[x[1]] == "K" or BOARD[x[2]] == "K" or BOARD[x[3]] == "K" or BOARD[x[4]] == "K":  # Rule 5
                return False
        if BOARD[x[0]] == "Q":
            if BOARD[x[1]] != "J" and BOARD[x[2]] != "J" and BOARD[x[3]] != "J" and BOARD[x[4]] != "J":  # Rule 3
                return False
            if BOARD[x[1]] == "Q" or BOARD[x[2]] == "Q" or BOARD[x[3]] == "Q" or BOARD[x[4]] == "Q":  # Rule 5
                return False
        if BOARD[x[0]] == "J":
            if BOARD[x[1]] == "J" or BOARD[x[2]] == "J" or BOARD[x[3]] == "J" or BOARD[x[4]] == "J":  # Rule 5
                return False
    return True  # Board is valid


generate_options()


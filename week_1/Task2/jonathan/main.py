import string
import random
import os
import copy

class Board:

    def __init__(self, playground):
        self.playground = playground
        self.path = []
    
    def add_child(self, child):
        child.path = self.path + [self.playground]
        return child

def prepare_data(data):
    file = data
    A_DATA, B_DATA = sorted([word[:e] for word in file for e in range(len(word))]), sorted([word for word in file for e in range(len(word))])
    return set(A_DATA), set(B_DATA)
    # A_DATA = {word.rstrip(): sorted({word[:e] for e in range(len(word)) if e != 0 and e != len(word) - 1}) for word in file}
    # return A_DATA

neighborOffsets = ((-1, -1), (-1, 0), (-1, 1),(0, -1), (0, 0), (0, 1),(1, -1), (1, 0), (1, 1),)

def solve_board_with_data(board, prefixes, full_words, found, state=None):
    for e in range(len(board.playground)):
        for i in range(len(board.playground[e])):
            if state: # search next from this state
                for e in neighborOffsets:
                    pass
            if not state: # search new letter
                if board.playground[e][i][1] == 0 and board.playground[e][i][0] in prefixes:
                    new_board = board.add_child(copy.deepcopy(board))
                    new_board.playground[e][i][1] = (e + 1) * (i + 1)
                    solve_board_with_data(new_board, prefixes, full_words, found, new_board.playground[e][i][1])
                    
    return False

if __name__ == "__main__":
    board = Board([[[random.choice(string.ascii_lowercase), 0] for e in range(5)] for e in range(5)])
    print(board.playground)
    prefixes, full_words = prepare_data(open(os.getcwd() + "\\week_1\\Task2\\jonathan\\words.txt", "r"))
    answers = solve_board_with_data(board, prefixes, full_words, [])
    print(answers)
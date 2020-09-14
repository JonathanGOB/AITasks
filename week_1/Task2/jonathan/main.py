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

    def __str__(self):
        display = []
        for row in self.playground:
            row_list = []
            for column in row:
                row_list.append(column[0])
            display.append(" ".join(row_list))
        return '\n'.join(display)

def prepare_data(data):
    file = data
    A_DATA, B_DATA = sorted([word[:e] for word in file for e in range(len(word))]), sorted([word for word in file for e in range(len(word))])
    return set(A_DATA), set(B_DATA)
    # A_DATA = {word.rstrip(): sorted({word[:e] for e in range(len(word)) if e != 0 and e != len(word) - 1}) for word in file}
    # return A_DATA

neighborOffsets = (
		         (-1, 0),
		(0, -1), (0, 0), (0, 1),
		        (1, 0),)

def solve_board_with_data(board, prefixes, full_words, found, word=None, state=None):
    print(word)
    if state: # search next from this state
        for e in neighborOffsets:
            temp = copy.deepcopy(state)
            if state[0] == len(board.playground) - 1 and e[0] == 1:
                temp[0] = -1
            if state[1] == len(board.playground) - 1 and e[1] == 1:
                temp[1] = -1
            if board.playground[e[0] + temp[0]][e[1] + temp[1]][1] == 0: 
                if word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0] in prefixes or word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0] in full_words:
                    new_board = board.add_child(copy.deepcopy(board)) 
                    new_board.playground[e[0] + temp[0]][e[1] + temp[1]][1] == (temp[0] + 1) * (temp[1] + 1)
                    if word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0] in prefixes:
                        solve_board_with_data(new_board, prefixes, full_words, found, word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0], [temp[0], temp[1]])
                    if word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0] in full_words:
                        found.append(new_board)
                        solve_board_with_data(new_board, prefixes, full_words, found)

    if not state: # search new letter
        for e in range(len(board.playground)):
            for i in range(len(board.playground[e])):
                    if board.playground[e][i][1] == 0 and board.playground[e][i][0] in prefixes:
                        new_board = board.add_child(copy.deepcopy(board))
                        new_board.playground[e][i][1] = (e + 1) * (i + 1)
                        solve_board_with_data(new_board, prefixes, full_words, found, new_board.playground[e][i][0], [e, i])
    
    return found

if __name__ == "__main__":
    board = Board([[[random.choice(string.ascii_lowercase), 0] for e in range(5)] for e in range(5)])
    print(board)
    prefixes, full_words = prepare_data(open(os.getcwd() + "\\week_1\\Task2\\jonathan\\words.txt", "r"))
    answers = solve_board_with_data(board, prefixes, full_words, [])
    print(answers)
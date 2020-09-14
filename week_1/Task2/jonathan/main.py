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

def prepare_data(file_A, file_B):
    A_DATA = sorted([word[:e] for word in file_A for e in range(len(word)) if e < len(word) - 1 and e != 0])
    B_DATA = sorted([word.rstrip("\n") for word in file_B])
    return set(A_DATA), set(B_DATA)

neighborOffsets = ((-1, 0),(0, -1), (0, 0), (0, 1),(1, 0),)

def solve_board_with_data(board, prefixes, full_words, found, word=None, state=None, start_position=None):
    if start_position: # search next from this state
        for e in neighborOffsets:
            temp = copy.deepcopy(state)
            if state[0] == len(board.playground) - 1 and e[0] == 1:
                temp[0] = -1
            if state[1] == len(board.playground) - 1 and e[1] == 1:
                temp[1] = -1
            if board.playground[e[0] + temp[0]][e[1] + temp[1]][1] == 0: 
                if word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0] in prefixes or word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0] in full_words:
                    new_board = board.add_child(copy.deepcopy(board)) 
                    new_board.playground[e[0] + temp[0]][e[1] + temp[1]][1] = (start_position[0] + 1) * (start_position[1] + 1)
                    if word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0] in prefixes:
                        solve_board_with_data(new_board, prefixes, full_words, found, word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0], [e[0] + temp[0], e[1] + temp[1]], start_position)
                    if word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0] in full_words and word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0] not in found:
                        found.append(word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0])
                        solve_board_with_data(new_board, prefixes, full_words, found)

    if not start_position: # search new letter
        for e in range(len(board.playground)):
            for i in range(len(board.playground[e])):
                    if board.playground[e][i][1] == 0 and board.playground[e][i][0] in prefixes:
                        new_board = board.add_child(copy.deepcopy(board))
                        new_board.playground[e][i][1] = (e + 1) * (i + 1)
                        solve_board_with_data(new_board, prefixes, full_words, found, new_board.playground[e][i][0], [e, i], [e, i])
    
    return found

def solve_easy(board,  prefixes, full_words, found, word=None, state=None, start_position=None):
    if start_position: # search next from this state
        for e in neighborOffsets:
            temp = copy.deepcopy(state)
            if state[0] == len(board.playground) - 1 and e[0] == 1:
                temp[0] = -1
            if state[1] == len(board.playground) - 1 and e[1] == 1:
                temp[1] = -1
            if word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0] in prefixes or word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0] in full_words:
                new_board = board.add_child(copy.deepcopy(board)) 
                if word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0] in prefixes:
                    solve_board_with_data(new_board, prefixes, full_words, found, word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0], [e[0] + temp[0], e[1] + temp[1]], start_position)
                if word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0] in full_words and word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0] not in found:
                    found.append(word + board.playground[e[0] + temp[0]][e[1] + temp[1]][0])
                    solve_board_with_data(new_board, prefixes, full_words, found)

    if not start_position: # search new letter
        for e in range(len(board.playground)):
            for i in range(len(board.playground[e])):
                new_board = board.add_child(copy.deepcopy(board))
                new_board.playground[e][i][1] = (e + 1) * (i + 1)
                solve_board_with_data(new_board, prefixes, full_words, found, new_board.playground[e][i][0], [e, i], [e, i])
    
    return found
if __name__ == "__main__":
    board = Board([[[random.choice(string.ascii_lowercase), 0] for e in range(10)] for e in range(10)])
    print(board)
    prefixes, full_words = prepare_data(open(os.getcwd() + "\\week_1\\Task2\\jonathan\\words.txt", "r"), open(os.getcwd() + "\\week_1\\Task2\\jonathan\\words.txt", "r"))
    answers = solve_easy(board, prefixes, full_words, [])
    for answer in answers:
        print(answer)
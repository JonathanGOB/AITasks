import string
import random
import os
class Board:

    def __init__(self, length, height):
        self.playground = [[random.choice(string.ascii_lowercase) for e in range(length)] for e in range(height)]
    
    def __str__(self):
        display = []
        for row in self.playground:
            display.append(" ".join(row))
        return '\n'.join(display)

def prepare_data(data):
    file = data
    A_DATA = {word.rstrip(): sorted({word[:e] for e in range(len(word)) if e != 0}) for word in file}
    return A_DATA

def solve_board_with_data(board, data):
    
    pass 
if __name__ == "__main__":
    board = Board(5,5)
    print(board)
    data = prepare_data(open(os.getcwd() + "\\week_1\\Task2\\jonathan\\words.txt", "r"))
    print(data)
    answers = solve_board_with_data(board, data)
    print(answers)
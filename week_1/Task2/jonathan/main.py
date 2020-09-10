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
    A_DATA = [word if e == len(word) + 1 else word[:e] for word in file for e in range(len(word))]
    return set(A_DATA)


board = Board(5,5)
print(board)
print(prepare_data(open(os.getcwd() + "\\week_1\\Task2\\jonathan\\words.txt", "r")))
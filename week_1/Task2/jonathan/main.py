import string
import random

class Board:

    def __init__(self, length, height):
        self.playground = [[random.choice(string.ascii_lowercase) for e in range(length)] for e in range(height)]
    
    def __str__(self):
        display = []
        for row in self.playground:
            display.append(" ".join(row))
        return '\n'.join(display)

board = Board(5,5)
print(board)
class Board:

    def __init__(self, length, height):
        self.playground = [[] for e in range(height)]
        print(self.playground)

Board(5,5)
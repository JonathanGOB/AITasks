import string
import random

letters = string.ascii_lowercase
rows = []


def make_board(row_size, column_size):
    for x in range(column_size):
        row = []
        for y in range(row_size):
            row.append(random.choice(letters))
        rows.append(row)


make_board(10, 10)
for z in rows:
    print(z)


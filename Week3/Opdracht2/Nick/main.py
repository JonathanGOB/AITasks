import itertools

# Questions
# 1a 40320 calculate by 8!

# Rules
# 1. Each A has a H
# 2. Each H has a V
# 3. Each V has a B
# 4. Each A doesn't border a V
# 5. Same suit can't border each other


# TODO Domain 1 choose the easiest one
BOARD1 = {
    0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None
}
VALUES1 = ["A1", "A2", "H1", "H2", "D1", "D2", "B1", "B2"]

for values in list(itertools.permutations(VALUES1)):
    for index in range(8):
        BOARD1[index] = values[index]  # Generate a board option

test1 = BOARD1[0]

# TODO Domain 2 choose the easiest
BOARD2 = {
    "A1": None, "A2": None, "H1": None, "H2": None, "D1": None, "D2": None, "B1": None, "B2": None
}
VALUES2 = [0, 1, 2, 3, 4, 5, 6, 7]

for values in list(itertools.permutations(VALUES2)):
    index = 0
    for key in BOARD2.keys():
        BOARD2[key] = values[index]  # Generate a board option
        index += 1

test = BOARD2["A1"]


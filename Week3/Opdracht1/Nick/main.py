from itertools import permutations

FLOORS = [0, 1, 2, 3, 4]

# Rules
# 1. L == 4   False
# 2. M == 0   False
# 3. N == 4 or N == 0 False
# 4. E needs to be at least 1 higher than M
# 5. J can't be +1 or -1 apart from N
# 6. N can't be +1 or -1 apart from M

solutions = []

for (L, M, N, E, J) in list(permutations(FLOORS)):
    if L == 4:
        continue
    if M == 0:
        continue
    if N == 4 or N == 0:
        continue
    if E == 0 or E == 1:  # E need to live at least 1 higher than M, so floor 0 and 1 can't happen
        continue
    rule4 = M + 1
    if E < rule4:
        continue
    rule5 = [N-1, N+1]
    if E in rule5:
        continue
    rule6 = [M - 1, M + 1]
    if N in rule6:
        continue

    loes = (L, "Loes")
    marja = (M, "Marja")
    niels = (N, "Niels")
    erik = (E, "Erik")
    joep = (J, "Joep")

    solutions.append(sorted([loes, marja, niels, erik, joep]))

for solution in solutions:
    print(solution)





import math
from collections import namedtuple

#https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def two_opt(cities):
    i = 0
    while i < len(cities):
        if i + 1 == len(cities):
            selected = [cities[i], cities[0]]
        else:
            selected = [cities[i], cities[i + 1]]
        e = 0
        changed = False
        while e < len(cities):
            temp_selected = selected + [cities[e], cities[e + 1] if e + 1 < len(cities) else cities[0]]
            print(temp_selected, i, e)
            if temp_selected[1] == temp_selected[2] or temp_selected[3] == temp_selected[0] or temp_selected[0] == temp_selected[2] or temp_selected[3] == temp_selected[1]:
                e += 1
                continue
            if intersect(*temp_selected):
                index1 = cities.index(temp_selected[1])
                index2 = cities.index(temp_selected[3])
                cities[index2], cities[index1] = cities[index1], cities[index2]
                i = 0
                changed = True
            e += 1
        if not changed:
            i += 1
    return cities

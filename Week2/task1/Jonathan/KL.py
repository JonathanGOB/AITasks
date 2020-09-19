import math
from collections import namedtuple
import copy

#https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)

def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i-1])
               for i in range(len(tour)))

def two_opt(cities):
    i = 0
    cities = list(cities)
    normal_length = tour_length(cities)
    while i < len(cities):
        if i + 1 == len(cities):
            selected = [cities[i], cities[0]]
        else:
            selected = [cities[i], cities[i + 1]]
        e = 0
        changed = False
        while e < len(cities):
            ch = False
            temp_selected = selected + [cities[e], cities[e + 1] if e + 1 < len(cities) else cities[0]]
            print(temp_selected, i, e)
            if temp_selected[1] == temp_selected[2] or temp_selected[3] == temp_selected[0] or temp_selected[0] == temp_selected[2] or temp_selected[3] == temp_selected[1]:
                e += 1
                continue
            if intersect(*temp_selected):
                index1 = cities.index(temp_selected[1])
                index2 = cities.index(temp_selected[3])
                check_list = copy.deepcopy(cities)
                check_list[index2], check_list[index1] = check_list[index1], check_list[index2]
                if tour_length(check_list) < normal_length:
                    cities[index2], cities[index1] = cities[index1], cities[index2]
                    normal_length = tour_length(cities)
                    i = 0
                    e = 0
                    changed = True
                    ch = True
            if not ch:
                e += 1
        if not changed:
            i += 1
    return cities

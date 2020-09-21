import math

import numpy as np


def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)


def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i - 1])
               for i in range(len(tour)))


# (y2 - y1)*(x3 - x2) - (y3 - y2)*(x2 - x1) #https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/%c2%a0/
def orientation(p1, p2, p3):
    val = (float(p2.y - p1.y) * (p3.x - p2.x)) - (float(p2.x - p1.x) * (p3.y - p2.y))
    if val > 0:
        return 1
    elif val < 0:
        return 2
    else:
        return 0


def is_intersect(p1, p2, q1, q2):
    op1 = orientation(p1, q1, p2)
    op2 = orientation(p1, q1, q2)
    op3 = orientation(p2, q2, p1)
    op4 = orientation(p2, q2, q1)

    if op1 != op2 and op3 != op4:
        return True
    return False


def onSegment(p, q, r):
    return distance(p, q) + distance(r, q) == distance(p, r)


def dist(city1, city2):
    dist = [(a - b) ** 2 for a, b in zip(city1, city2)]
    dist = math.sqrt(sum(dist))
    return dist


def two_opt(cities):
    minchange = -1
    while minchange < 0:
        minchange = 0
        for i in range(0, len(cities) - 2):
            for j in range(i + 2, len(cities) - 1):
                change = dist(cities[i], cities[j]) + dist(cities[i + 1], cities[j + 1]) - dist(cities[i], cities[
                    i + 1]) - dist(cities[j], cities[j + 1])
                if (minchange > change):
                    minchange = change;
                    cities[i + 1:j + 1] = cities[i + 1:j + 1][::-1]
    return cities

import math


def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)

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

    if op1 == 0 and onSegment(p1, p2, q1):
        return True
    if op2 == 0 and onSegment(p1, q2, q1):
        return True
    if op3 == 0 and onSegment(p2, p1, q2):
        return True
    if op4 == 0 and onSegment(p2, q1, q2):
        return True
    return False

def onSegment(p, q, r):
    return distance(p, q) + distance(r, q) == distance(p, r)

def two_opt(cities):
    i = 0
    while i + 4 != len(cities):
        selected = [cities[i], cities[i + 1]]
        e = 0
        changed = False
        while e + 4 != len(cities):
            if i != e and cities[e] != selected[1] or cities[0] != cities[e]:
                temp_selected = selected + [cities[e], cities[e + 1]]
                if is_intersect(*temp_selected):
                        print("switched {}, {} : {}, {} list : {}".format(*temp_selected, cities))
                        print(i, e)
                        cities[i + 1], cities[e + 1] = cities[e + 1], cities[i + 1]
                        i = 0
                        changed = True
            e += 1
        if not changed:
            i += 1
    return cities
import math

def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)

def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i-1])
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
    tour = list(cities)
    improved = True
    cache = tour_length(tour)
    while improved:
        improved = False
        for i in range(1, len(tour) - 2):
            selected = [tour[::-1][i], tour[::-1][i -1]]
            for j in range(i + 1, len(tour)):
                comparison = [tour[::-1][j], tour[::-1][j-1]]
                if comparison[0] == selected[0] or comparison[1] == selected[1] or j - i == 1:
                    continue
                if is_intersect(*selected, *comparison):
                    new_tour = tour[:]
                    new_tour[i:j] = tour[j-1:i-1:-1]
                    if tour_length(new_tour) < cache:
                        cache = tour_length(new_tour)
                        tour = new_tour
                        improved = True
    return tour
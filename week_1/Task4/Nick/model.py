import random
import heapq
import math

import week_1.Task4.Nick.config as cf

# global var
grid = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]


class PriorityQueue:
    # to be use in the A* algorithm
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    # in a min-heap, the keys of parent nodes are less than or equal to those
    # of the children and the lowest key is in the root node
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    # heap elements are tuples (priority, item)
    def put(self, priority, item):
        heapq.heappush(self.elements, (priority, item))

    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)[1]


class Node:

    def __init__(self, x, y, g=99999, f=99999, parent=None):
        self.x = x
        self.y = y
        self.g = g
        self.f = f
        self.parent = parent
        self.children = []
        self.blocked = False

    def __gt__(self, other):
        return self.x > other.x

    def generate_children(self, x, y):
        if y != 0:
            self.children.append(Node(x=x, y=y-1))  # Top child
        if x != cf.SIZE:
            self.children.append(Node(x=x+1, y=y))  # Right child
        if y != cf.SIZE:
            self.children.append(Node(x=x, y=y+1))  # Bottom child
        if x != 0:
            self.children.append(Node(x=x-1, y=y))  # Left child

    def check_blocked(self):
        for child in self.children:
            if child.x < cf.SIZE and child.y < cf.SIZE:
                if get_grid_value((child.x, child.y)) == "b":
                    child.blocked = True


def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get()) / 10 else 0


def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    return grid[node[0]][node[1]]


def set_grid_value(node, value):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    grid[node[0]][node[1]] = value


def heuristic(child):
    h = abs(child.x - (cf.SIZE-1)) + abs(child.y - (cf.SIZE-1))
    return h


def search(app, start, goal, alg):
    start_node = Node(x=start[0], y=start[1], g=0, f=0)
    open_set = PriorityQueue()
    open_set.put(0, start_node)
    test_open_set = [start_node]
    closed_set = []
    while len(open_set.elements) > 0:
        current = open_set.get()  # Get lowest score
        current.generate_children(current.x, current.y)
        current.check_blocked()
        if current.x == goal[0] and current.y == goal[1]:  # Check if current is the goal
            return draw_path(current, app)
        test_open_set.remove(current)
        closed_set.append(current)
        app.plot_node((current.x, current.y), color=cf.PATH_C)
        for child in current.children:
            if child in closed_set or child.blocked:  # Skip if already checked or path blocked
                continue
            temporary_g_score = current.g + 1
            if temporary_g_score < child.g:  # Path is better than previous one
                child.parent = current
                child.g = temporary_g_score
                child.f = child.g + heuristic(child)
                if child not in test_open_set:
                    test_open_set.append(child)
                    if alg == "UC":  # When UC alg is selected
                        open_set.put(child.g, child)
                    if alg == "A*":  # When A* alg is selected
                        open_set.put(child.f, child)
    return print("There is no solution")


def draw_path(current, app):
    temp = current
    while temp.parent:
        app.plot_line_segment(temp.x, temp.y, temp.parent.x, temp.parent.y, color=cf.FINAL_C)
        temp = temp.parent
        app.pause()

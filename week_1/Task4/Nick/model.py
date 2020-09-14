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

    def __init__(self, x, y, g=0, f=0, parent=None):
        self.x = x
        self.y = y
        self.g = g
        self.f = f
        self.parent = parent
        self.children = []

    def __gt__(self, other):
        return self.x > other.x

    def generate_children(self, x, y):
        if y != 0:
            self.children.append(Node(x, y - 1))  # Top child
        if x != cf.SIZE - 1:
            self.children.append(Node(x + 1, y))  # Right child
        if y != cf.SIZE - 1:
            self.children.append(Node(x, y + 1))  # Bottom child
        if x != 0:
            self.children.append(Node(x - 1, y))  # Left child


def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get()) / 10 else 0


def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    return grid[node[0]][node[1]]


def set_grid_value(node, value):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    grid[node[0]][node[1]] = value


def search(app, start, goal):  # TODO add heuristic
    start_node = Node(start[0], start[1])
    open_set = PriorityQueue()
    open_set.put(0, start_node)
    test_open_set = [start_node]
    closed_set = []
    while len(open_set.elements) > 0:
        current = open_set.get()  # Get lowest score
        current.generate_children(current.x, current.y)
        if current.x == goal[0] and current.y == goal[1]:  # Check if current is the goal
            return draw_path(current, app)
        closed_set.append(current)
        for child in current.children:
            if child in closed_set:
                continue  # Skip if already checked
            temporary_g_score = current.g + 1
            if child not in test_open_set:
                open_set.put(temporary_g_score, child)  # New node
                test_open_set.append(child)
            elif temporary_g_score > child.g:
                continue  # Not a better path
            child.parent = current
            child.g = temporary_g_score
            # child.f = child.g + heuristic() # TODO

    return print("There is no solution")


def draw_path(current, app):
    temp = current
    while temp.parent:
        app.plot_line_segment(temp.x, temp.y, temp.parent.x, temp.parent.y)
        temp = temp.parent

    # plot a sample path for demonstration
    # for i in range(cf.SIZE - 1):
    #     app.plot_line_segment(i, i + 1, i + 1, i + 1, color=cf.FINAL_C)
    #     app.plot_line_segment(i, i, i, i + 1, color=cf.FINAL_C)
    #
    #     app.pause()

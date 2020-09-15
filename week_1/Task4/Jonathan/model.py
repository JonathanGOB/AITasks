import random
import heapq
import math
import config as cf

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
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)[1]


def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get()) / 10 else 0


neighborOffsets = ((-1, 0), (0, -1), (0, 1), (1, 0),)


def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    return grid[node[0]][node[1]]


def set_grid_value(node, value):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    grid[node[0]][node[1]] = value


def manhattan_distance(current_node, goal):
    return abs(current_node[0] - goal[0]) + abs(current_node[1] - goal[1])


def search(app, start, goal):
    queue = PriorityQueue()
    closed_list = []
    queue.put([start, 0, 0, 0, [goal]], 0)  # G = distance, H = heuristic, F= total_cost, path
    while not queue.empty():
        node = queue.get()
        closed_list.append(node[0])
        for neighbor in neighborOffsets:
            if (node[0][0] + neighbor[0], node[0][1] + neighbor[1]) == goal:
                for k in range(len(node[4])):
                    app.plot_line_segment(node[4][k][0], node[4][k][1], node[4][k + 1][0], node[4][k + 1][1] + 1,
                                          color=cf.FINAL_C)
                while not queue.empty():
                    queue.get()
                continue
            if not (node[0][0] + neighbor[0], node[0][1] + neighbor[1]) in closed_list:
                if get_grid_value([node[0][0] + neighbor[0], node[0][1] + neighbor[1]]) != 'b':
                    if (node[0][0] + neighbor[0] != len(grid[0]) - 1 and not node[0][0] + neighbor[0] < 0) and (
                            node[0][1] + neighbor[1] != len(grid[0]) - 1 and not node[0][1] + neighbor[1] < 0):
                        G = node[1] + 1
                        H = manhattan_distance((node[0][0] + neighbor[0], node[0][1] + neighbor[1]), goal)
                        F = G + H
                        path = node[:][4]
                        path.append((node[0][0] + neighbor[0], node[0][1] + neighbor[1]))
                        queue.put([(node[0][0] + neighbor[0], node[0][1] + neighbor[1]), G, H, F, path], F)

    # plot a sample path for demonstration
    # for i in range(cf.SIZE - 1):
    #     app.plot_line_segment(i, i, i, i + 1, color=cf.FINAL_C)
    #     app.plot_line_segment(i, i + 1, i + 1, i + 1, color=cf.FINAL_C)
    #     app.pause()

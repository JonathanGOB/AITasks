import random
import heapq
import math
import config as cf
import copy

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
        print(node[4])
        closed_list.append(node[0])
        #print(node[0])
        for neighbor in neighborOffsets:
            key = True
            if (node[0][0] + neighbor[0], node[0][1] + neighbor[1]) == goal:
                node[4] = [start] + node[4]
                print(node[4])
                for k in range(len(node[4])):
                    if k != len(node[4]) - 1:
                        app.plot_line_segment(node[4][k][0], node[4][k][1], node[4][k + 1][0], node[4][k + 1][1],
                                              color=cf.FINAL_C)
                while not queue.empty():
                    queue.get()
                continue
            for closed_child in closed_list:
                if (node[0][0] + neighbor[0], node[0][1] + neighbor[1]) == closed_child:
                    key = False
                    break
            if node[0][0] + neighbor[0] > len(grid[0]) - 1 or node[0][0] + neighbor[0] < 0 or node[0][1] + neighbor[1] > len(grid[0]) - 1 or node[0][1] + neighbor[1] < 0:
                continue
            if get_grid_value([node[0][0] + neighbor[0], node[0][1] + neighbor[1]]) != 'b':
                G = copy.deepcopy(node[1]) + 1
                H = manhattan_distance((node[0][0] + neighbor[0], node[0][1] + neighbor[1]), goal)
                F = G + H
                path = copy.deepcopy(node[4])
                path.insert(len(path) - 1, (node[0][0] + neighbor[0], node[0][1] + neighbor[1]))
                for element in queue.elements:
                    if element[1][0] == (node[0][0] + neighbor[0], node[0][1] + neighbor[1]) and G < element[1][1]:
                        print("checked")
                        key = False
                        break
                if key:
                    queue.put([(node[0][0] + neighbor[0], node[0][1] + neighbor[1]), G, H, F, path], F)

    # plot a sample path for demonstration
    # for i in range(cf.SIZE - 1):
    #     app.plot_line_segment(i, i, i, i + 1, color=cf.FINAL_C)
    #     app.plot_line_segment(i, i + 1, i + 1, i + 1, color=cf.FINAL_C)
    #     app.pause()

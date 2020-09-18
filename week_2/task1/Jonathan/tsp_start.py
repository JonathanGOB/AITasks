import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from collections import namedtuple
import heapq

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')

def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)

def nearest_neighbour(cities):
    cities = list(cities)
    length = len(cities)
    path = [cities[0]]
    del cities[0]
    while len(path) != length:
        temp = []
        for city in cities:
            heapq.heappush(temp, (distance(city, path[len(path) - 1]), city))
        city = heapq.heappop(temp)[1]
        path.insert(len(path), city)
        cities.remove(city)
    return path


def try_all_tours(cities):
    # generate and test all possible tours of the cities and choose the shortest tour
    tours = alltours(cities)
    return min(tours, key=tour_length)

def alltours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # cities is a set, sets don't support indexing
    start = next(iter(cities))
    return [[start] + list(rest)
            for rest in itertools.permutations(cities - {start})]

def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i-1]) 
               for i in range(len(tour)))

def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed(n) # the current system time is used as a seed
    # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height))
                     for c in range(n))

def plot_tour(tour): 
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-')
    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()

def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.process_time()
    tour = algorithm(cities)
    t1 = time.process_time()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)

cities = make_cities(10)
NN = nearest_neighbour(cities)
TAT = try_all_tours(cities)
res = [1 if NN[N] == TAT[N] else 0 for N in range(len(NN))].count(1) / len([1 if NN[N] == TAT[N] else 0 for N in range(len(NN))]) * 100
print("{0} % similarity".format(res))
plot_tsp(nearest_neighbour, make_cities(10))

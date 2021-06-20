import math
from random import random

def random_cities(count, scaling):
    return [(x, scaling*random(), scaling*random()) for x in range(count)]

def calc_distance(a, b):
    delta_x = a[1] - b[1]
    delta_y = a[2] - b[2]

    return math.sqrt( (delta_x ** 2) + (delta_y ** 2) )
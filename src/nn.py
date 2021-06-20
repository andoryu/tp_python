
from common import calc_distance


def calc_paths(cities):

    order = []
    distance = 0.0

    current = cities[0]
    order.append(current)
    rest = cities[1:]

    while rest:
        distance_data = sort_cities(calc_distances(current, rest))
        distance += distance_data[0][1]

        #first city in list, first field in tuple = city
        current = distance_data[0][0]
        order.append(current)
        rest = [c[0] for c in distance_data[1:]]

    order.append(cities[0])
    distance += calc_distance(order[-2], order[-1])

    path_list = [c[0] for c in order]

    return (path_list, distance)


def sort_cities(cities):
    return sorted(cities, key=(lambda a : a[1]) )


def calc_distances(source, cities):
    return [ (c, calc_distance(source, c)) for c in cities]

from math import pow, sqrt


def edit_distance(graph1: tuple, graph2: tuple):
    return 0


def euclidean(graph1: tuple[list, list], graph2: tuple[list, list]):
    n_vertexes = len(graph1[0])

    distance = 0
    for v in range(n_vertexes):
        x1, y1, z1 = graph1[0][v]
        x2, y2, z2 = graph2[0][v]

        distance += sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2))

    return distance

from math import pow, sqrt
from graph.essential import Graph


def edit_distance(graph1: Graph, graph2: Graph):
    return 0


def euclidean(graph1: Graph, graph2: Graph):
    n_vertexes = graph1.vertexes_count

    distance = 0
    for v in range(n_vertexes):
        x1, y1, z1, _ = graph1.get_vertex(v)
        x2, y2, z2, _ = graph2.get_vertex(v)

        distance += sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2))

    return distance

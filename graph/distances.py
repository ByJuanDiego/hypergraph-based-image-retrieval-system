from math import pow, sqrt, log2
from numpy import array, dot
from numpy.linalg import norm
from graph.essential import Graph


def cosine_score(
        graph1: Graph,
        graph2: Graph
) -> float:
    edges = graph1.get_edges()
    distance = 0

    for u, v in edges:
        vertex_u1, vertex_v1 = graph1.get_vertex(u), graph1.get_vertex(v)
        vertex_u2, vertex_v2 = graph2.get_vertex(u), graph2.get_vertex(v)

        v1 = array([(vertex_v1[0] - vertex_u1[0]), (vertex_v1[1] - vertex_u1[1]), (vertex_v1[2] - vertex_u1[2])])
        v2 = array([(vertex_v2[0] - vertex_u2[0]), (vertex_v2[1] - vertex_u2[1]), (vertex_v2[2] - vertex_u2[2])])

        distance += (1 - dot(v1, v2) / (norm(v1) * norm(v2)))

    return distance


def euclidean_distance(
        graph1: Graph,
        graph2: Graph
) -> float:
    n_vertexes = graph1.vertexes_count

    distance = 0
    for v in range(n_vertexes):
        x1, y1, z1, _ = graph1.get_vertex(v)
        x2, y2, z2, _ = graph2.get_vertex(v)

        distance += sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2))

    return distance


def weighted_distance(
        graph1: Graph,
        graph2: Graph,
        k: float = 0.5
) -> float:
    return cosine_score(graph1, graph2) + (k * euclidean_distance(graph1, graph2))


def log_weighted_distance(
        graph1: Graph,
        graph2: Graph,
) -> float:
    return cosine_score(graph1, graph2) * log2(euclidean_distance(graph1, graph2) + 1)


def manhattan_distance(
        graph1: Graph,
        graph2: Graph
) -> float:
    n_vertexes = graph1.vertexes_count

    distance = 0
    for v in range(n_vertexes):
        x1, y1, z1, _ = graph1.get_vertex(v)
        x2, y2, z2, _ = graph2.get_vertex(v)

        distance += abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)

    return distance


def l2_distance(
        graph1: Graph,
        graph2: Graph
) -> float:
    array1 = array(graph1.get_vertexes())
    array2 = array(graph2.get_vertexes())

    return norm(array1 - array2)


def l2__distance(
        graph1: Graph,
        graph2: Graph
) -> float:
    arr1 = array(list(map(lambda x: array(x[:3]) * x[3], graph1.get_vertexes())))
    arr2 = array(list(map(lambda x: array(x[:3]) * x[3], graph2.get_vertexes())))
    return norm(arr1 - arr2)


def cosine_v_distance(
        graph1: Graph,
        graph2: Graph
) -> float:
    arr1 = array(list(map(lambda x: array(x[:3]) * x[3], graph1.get_vertexes())))
    arr2 = array(list(map(lambda x: array(x[:3]) * x[3], graph2.get_vertexes())))
    return 1 - dot(arr1.reshape(-1), arr2.reshape(-1)) / (norm(arr1) * norm(arr2))

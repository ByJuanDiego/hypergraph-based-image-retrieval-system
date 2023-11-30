import timeit

from typing import List, Callable
from graph.essential import Graph, Cluster
from indexing.indexes import HyperGraph


def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = timeit.default_timer()
        result = func(*args, **kwargs)
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        print(f"Execution time of {func.__name__}: {execution_time} seconds")
        return result

    return wrapper


class KNN:
    _hypergraph: HyperGraph
    _distance_fn: Callable[[Graph, Graph], float]
    _threshold: float

    def __init__(
            self,
            hypergraph: HyperGraph,
    ) -> None:
        self._hypergraph = hypergraph
        self._distance_fn = hypergraph.get_distance()
        self._threshold = hypergraph.get_threshold()

    def query(self, query: Graph, k: int) -> List[str]:
        if k == 0:
            return []

        cluster: Cluster = min(self._hypergraph.get_clusters(),
                               key=lambda c: self._distance_fn(c.get_centroid(), query))

        sorted_paths = sorted(cluster.get_graphs(), key=lambda g: self._distance_fn(g, query))
        n = min(k, len(sorted_paths))

        return [graph.get_path() for graph in sorted_paths[:n]]


@measure_execution_time
def knn_retrieval(hyper_graph: HyperGraph, query: Graph, k: int):
    knn = KNN(hyper_graph)
    return knn.query(query, k)

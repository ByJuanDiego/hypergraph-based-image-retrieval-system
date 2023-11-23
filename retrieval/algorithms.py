from typing import List, Callable
from graph.essential import Graph, Cluster
from indexing.indexes import HyperGraph


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

        retrieval: List[str] = []
        clusters: List[Cluster] = sorted(self._hypergraph.get_clusters(),
                                         key=lambda c: self._distance_fn(c.get_centroid(), query))

        for cluster in clusters:
            graphs = sorted(cluster.get_graphs(), key=lambda g: self._distance_fn(g, query))

            for graph in graphs:
                retrieval.append(graph.get_path())

                if len(retrieval) >= k:
                    return retrieval

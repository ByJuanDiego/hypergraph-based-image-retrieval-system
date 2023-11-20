from typing import List, Callable
from graph.essential import Graph, Cluster
from indexing.indexes import HyperGraph


class KNN:
    _hypergraph: HyperGraph
    _distance: Callable[[Graph, Graph], float]

    def __init__(
            self,
            hypergraph: HyperGraph
    ) -> None:
        self._hypergraph = hypergraph
        self._distance = hypergraph.get_distance_callable()

    def query(self, query: Graph, k: int) -> List[str]:
        clusters = self._hypergraph.get_clusters()

        nearest_cluster: Cluster = min(clusters, key=lambda cluster: self._distance(cluster.get_centroid(), query))
        return []

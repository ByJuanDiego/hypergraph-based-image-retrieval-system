from graph.essential import Graph, Cluster
from typing import List, Callable

import pickle


class HyperGraph:
    _clusters: List[Cluster] = []
    _graphs: List[Graph]
    _centroids: List[Graph]
    _distance: Callable[[Graph, Graph], float]
    _threshold: float

    def __init__(
            self,
            graphs,
            centroids,
            distance,
            threshold
    ) -> None:
        self._graphs = graphs
        self._centroids = centroids
        self._distance = distance
        self._threshold = threshold

    def fit(
            self
    ) -> None:
        self._clusters = []

        for centroid in self._centroids:
            cluster = Cluster()
            cluster.set_centroid(centroid)
            self._clusters.append(cluster)

        for cluster in self._clusters:
            for graph in self._graphs:
                if graph.get_path() == cluster.get_centroid().get_path():
                    continue
                if self._distance(graph, cluster.get_centroid()) < self._threshold:
                    cluster.add_graph(graph)

    def get_clusters(
            self
    ) -> List[Cluster]:
        return self._clusters

    def get_distance_callable(
            self
    ) -> Callable[[Graph, Graph], float]:
        return self._distance

    def save_clusters(
            self,
            dir_path,
            filename
    ) -> None:
        with open(dir_path + "/" + filename, "wb") as file:
            pickle.dump(self.get_clusters(), file)

    def load_clusters(
            self,
            dir_path,
            filename
    ) -> None:
        with open(dir_path + "/" + filename, "rb") as file:
            self._clusters = pickle.load(file)

    def pretty_print(
            self
    ) -> None:
        for cluster in self.get_clusters()[20:30]:
            print(f"{cluster.get_centroid().get_path()}")
            print(f"{list(map(lambda graph: graph.get_path(), cluster.get_graphs()))}")

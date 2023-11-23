from graph.essential import Graph, Cluster
from typing import List, Callable, Tuple
import pickle
from random import sample


class HyperGraph:
    _graphs: List[Graph]
    _clusters: List[Cluster] = []
    _centroids: List[Graph]
    _distance: Callable[[Graph, Graph], float]
    _threshold: float

    # measurements
    _overlapping: float
    _density: float

    def __init__(
            self,
            graphs,
            distance,
            threshold,
            centroids
    ) -> None:
        self._graphs = graphs
        self._centroids = centroids
        self._distance = distance
        self._threshold = threshold
        self._overlapping = 0.0
        self._density = 0.0

    def fit(
            self
    ) -> None:
        self._clusters = []
        self._overlapping = 0.0

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
            self._overlapping += len(cluster.get_graphs())

        n_clusters = len(self._clusters)
        n_graphs = len(self._graphs)

        self._overlapping = self._overlapping / n_graphs
        self._density = n_clusters / n_graphs

    def get_clusters(
            self
    ) -> List[Cluster]:
        return self._clusters

    def get_overlapping(
            self
    ) -> float:
        return self._overlapping

    def get_density(
            self
    ) -> float:
        return self._density

    def get_distance(
            self
    ) -> Callable[[Graph, Graph], float]:
        return self._distance

    def get_threshold(
            self
    ) -> float:
        return self._threshold

    def save_clusters(
            self,
            dir_path,
            filename
    ) -> None:
        with open(dir_path + "/" + filename, "wb") as file:
            data: Tuple[List[Cluster], float, float] = (self._clusters, self._overlapping, self._density)
            pickle.dump(data, file)

    def load_clusters(
            self,
            dir_path,
            filename
    ) -> None:
        with open(dir_path + "/" + filename, "rb") as file:
            data: Tuple[List[Cluster], float, float] = pickle.load(file)
            self._clusters = data[0]
            self._overlapping = data[1]
            self._density = data[2]

    def pretty_print(
            self,
            k: int = 10
    ) -> None:

        for cluster in sample(self.get_clusters(), k):
            print(f"{cluster.get_centroid().get_path()}")
            for graph in cluster.get_graphs():
                print(f"\t{graph.get_path()}")
            print()

        print("measurements:")
        print(f"\toverlapping: {self.get_overlapping()}")
        print(f"\tdensity: {self.get_density()}")
        print(f"\tnumber of clusters: {len(self._clusters)}")

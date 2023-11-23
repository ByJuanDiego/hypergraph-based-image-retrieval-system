from graph.essential import Graph, Cluster
from typing import List, Callable, Tuple
import pickle


class HyperGraph:
    _clusters: List[Cluster] = []
    _overlapping: List[List[Tuple[int, float]]]
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

        print("--- start ---")
        for centroid in self._centroids:
            cluster = Cluster()
            cluster.set_centroid(centroid)
            self._clusters.append(cluster)

        for graph in self._graphs:
            for cluster in self._clusters:
                if graph.get_path() == cluster.get_centroid().get_path():
                    continue
                if self._distance(graph, cluster.get_centroid()) < self._threshold:
                    cluster.add_graph(graph)

        print("--- end1 ---")

        # Overlapping measurements (for hyper-graph navigation purposes)

        print("overlap")
        n = len(self._clusters)
        self._overlapping = [[] for _ in range(n)]

        for i in range(n):
            for j in range(i + 1, n):
                c1_paths = [graph.get_path() for graph in self._clusters[i].get_graphs()]
                c2_paths = [graph.get_path() for graph in self._clusters[j].get_graphs()]

                overlap = len([path for path in c1_paths if path in c2_paths])

                if overlap > 0:
                    self._overlapping[i].append((j, overlap))
                    self._overlapping[j].append((i, overlap))

        for i in range(n):
            self._overlapping[i].sort(key=lambda x: x[1])

        print("--- end2 ---")

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
            data: Tuple[List[Cluster], List[List[Tuple[int, float]]]] = (self._clusters, self._overlapping)
            pickle.dump(data, file)

    def load_clusters(
            self,
            dir_path,
            filename
    ) -> None:
        with open(dir_path + "/" + filename, "rb") as file:
            data: Tuple[List[Cluster], List[List[Tuple[int, float]]]] = pickle.load(file)
            self._clusters = data[0]
            self._overlapping = data[1]

    def pretty_print(
            self
    ) -> None:
        for cluster in self.get_clusters():

            print(f"{cluster.get_centroid().get_path()}")
            print(f"{list(map(lambda graph: graph.get_path(), cluster.get_graphs()))}")
            print()

        #
        # for x in self._overlapping:
        #     if x:
        #         print(x[len(x) - 1])

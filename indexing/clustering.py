import sys
import pickle


from typing import List, Annotated, Union
from graph.essential import Graph


class Cluster:
    _centroid: Union[Graph, None]
    _graphs: List[Graph]

    def __init__(self) -> None:
        self._centroid = None
        self._graphs = []

    def clear(self) -> None:
        self._graphs.clear()
        self._centroid = None

    def set_centroid(self, graph: Graph) -> None:
        self._centroid = graph
        self._graphs = [graph]

    def add_graph(self, graph: Graph) -> None:
        self._graphs.append(graph)

    def get_graphs(self) -> List[Graph]:
        return self._graphs

    def get_centroid(self) -> Graph:
        return self._centroid

    def size(self) -> int:
        return len(self._graphs)


class MeanShift:
    _threshold: float = 0
    _centroids: set[str] = []
    _graphs: dict = {}
    _distance = None
    _clusters = list[Cluster]

    def __init__(self, graphs: dict, distance_function, threshold: float):
        self._threshold = threshold
        self._centroids = set()
        self._graphs = graphs
        self._distance = distance_function

    def median_graph(
            self,
            s: list,  # list of graphs [("path", graph), ...]
    ) -> int:
        n = len(s)
        median_graph = None
        sum_of_distances = sys.maxsize

        for i in range(n):
            current_sum = 0

            for j in range(n):
                current_sum += self._distance(s[i][1], s[j][1])

            if current_sum < sum_of_distances:
                median_graph = i
                sum_of_distances = current_sum

        return median_graph

    def farthest(self, s: list, seed: int) -> int:
        n = len(s)
        farthest = None
        distance = -1

        for i in range(n):
            if current_distance := self._distance(s[seed][1], s[i][1]) > distance:
                farthest = i
                distance = current_distance

        return farthest

    def fit_centroids(self):
        s = list(self._graphs.items())
        self._centroids = set()

        while len(s) > 0:
            print(len(s))
            median_graph: int = self.median_graph(s)

            prototype: int = self.farthest(s, median_graph)
            prototype_path, prototype_graph = s[prototype]

            cluster = Cluster()
            cluster.set_centroid((prototype_path, prototype_graph))

            while True:
                for path, graph in s:
                    if path == prototype_path:
                        continue

                    is_cluster_member = True

                    for cluster_member_graph in cluster.get_entries():
                        if self._distance(graph, cluster_member_graph) > self._threshold:
                            is_cluster_member = False
                            break

                    if is_cluster_member:
                        cluster.add_entry((path, graph))

                cluster_entries: list[tuple] = cluster.get_entries()
                cluster_paths: set = {g[0] for g in cluster_entries}

                new_prototype: int = self.median_graph(cluster_entries)
                new_prototype_path, new_prototype_graph = cluster_entries[new_prototype]

                if new_prototype_path == prototype_path:
                    self._centroids.add(prototype_path)
                    print(f"path: {prototype_path}, size: {cluster.size()}")
                    s = [g for g in s if g[0] not in cluster_paths]
                    break

                print(f"size: {cluster.size()}")

                prototype_path, prototype_graph = new_prototype_path, new_prototype_graph
                cluster = Cluster()
                cluster.set_centroid((prototype_path, prototype_graph))

    def get_centroids(self):
        if not self._centroids:
            raise AttributeError("The clusters.p are empty!")
        return self._centroids

    def save_centroids(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.get_centroids(), file)

    def load_centroids(self, filename):
        with open(filename, "rb") as file:
            self._centroids = pickle.load(file)

    def fit_clusters(self):
        self._clusters = []

        for centroid_path in self._centroids:
            cluster = Cluster()
            cluster.set_centroid((centroid_path, self._graphs[centroid_path]))
            self._clusters.append(cluster)

        for cluster in self._clusters:
            for path, graph in self._graphs.items():
                if path == cluster.get_centroid()[0]:
                    continue
                if self._distance(graph, cluster.get_centroid()[1]) < self._threshold:
                    cluster.add_entry((path, graph))

    def get_clusters(self):
        return self._clusters

    def save_clusters(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.get_clusters(), file)

    def load_clusters(self, filename):
        with open(filename, "rb") as file:
            self._clusters = pickle.load(file)

    def pretty_print(self):
        for cluster in self._clusters:
            print(cluster.get_centroid()[0])
            for path, _ in cluster.get_entries():
                print(f"\t{path}")

    def knn(self, query):
        nearest = None
        distance = sys.maxsize

        selected_cluster = None
        for cluster in self._clusters:
            if cluster.get_centroid()[0] == query:
                selected_cluster = cluster

        for path, graph in selected_cluster.get_entries():
            if path == query:
                continue

            d = self._distance(selected_cluster.get_centroid()[1], graph)
            if d < distance:
                distance = d
                nearest = path

        return nearest

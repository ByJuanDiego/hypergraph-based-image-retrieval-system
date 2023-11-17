from graph.essential import Graph, Cluster
from typing import List, Callable

import pickle


class HyperGraph:
    _clusters: List[Cluster] = []
    _graphs: List[Graph]
    _centroids: List[Graph]
    _distance: Callable[[Graph, Graph], float]
    _threshold: float

    def __init__(self, graphs, centroids, distance, threshold):
        self._graphs = graphs
        self._centroids = centroids
        self._distance = distance
        self._threshold = threshold

    def fit(self):
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

    def get_clusters(self):
        return self._clusters

    def save_clusters(self, dir_path, filename):
        with open(dir_path + "/" + filename, "wb") as file:
            pickle.dump(self.get_clusters(), file)

    def load_clusters(self, dir_path, filename):
        with open(dir_path + "/" + filename, "rb") as file:
            self._clusters = pickle.load(file)

    def pretty_print(self):
        for cluster in self._clusters:
            print(cluster.get_centroid().get_path())
            for graph in cluster.get_graphs():
                print(f"\t{graph.get_path()}")

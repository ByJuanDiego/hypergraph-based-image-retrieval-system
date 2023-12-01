from multiprocess import pool

from typing import Callable, List, Dict, Tuple
from graph.essential import Graph, Cluster
from dataset.pickle import load_centroids, dump_centroids


class MeanShift:
    _threshold: float = 0
    _centroids: List[Graph] = []
    _graphs: List[Graph] = []
    _distance: Callable[[Graph, Graph], float] = None
    _distances_cache: Dict[Tuple[str, str], float] = {}

    def __init__(
            self,
            graphs: List[Graph],
            threshold: float,
            distance_function: Callable[[Graph, Graph], float],
            distance_cache: Dict[Tuple[str, str], float] = None
    ) -> None:

        def optimized_distance(g1: Graph, g2: Graph) -> float:
            if self._distance is not None and (g1.get_path(), g2.get_path()) in self._distances_cache:
                return self._distances_cache[(g1.get_path(), g2.get_path())]

            dist = distance_function(g1, g2)

            self._distances_cache[(g2.get_path(), g1.get_path())] = dist
            self._distances_cache[(g1.get_path(), g2.get_path())] = dist
            return dist

        self._threshold = threshold
        self._graphs = graphs
        self._distance = optimized_distance

        if distance_cache is not None:
            self._distances_cache = distance_cache

    def calculate_distance(
            self,
            args: Tuple[int, List[Graph]]
    ) -> Tuple[int, float]:
        i, s = args
        distances_sum = 0
        n = len(s)

        for j in range(n):
            if i == j:
                continue
            distances_sum += self._distance(s[i], s[j])

        return i, distances_sum

    def median_graph(
            self,
            s: List[Graph]
    ) -> int:
        n: int = len(s)

        with pool.Pool() as executor:
            futures = [(i, s) for i in range(n)]
            results = executor.map(self.calculate_distance, futures)

        median_graph_index, _ = min(results, key=lambda x: x[1])

        return median_graph_index

    def farthest(
            self,
            s: List[Graph],
            seed: int
    ) -> int:
        n: int = len(s)
        farthest_graph_index: int = -1
        distance: float = -1

        for i in range(n):
            if current_distance := self._distance(s[seed], s[i]) > distance:
                farthest_graph_index = i
                distance = current_distance

        return farthest_graph_index

    def fit(
            self,
            max_iter: int = 100
    ) -> None:
        s: List[Graph] = self._graphs.copy()
        self._centroids.clear()

        def process_graph(graph, threshold):
            is_cluster_member = True
            for cluster_member_graph in cluster.get_graphs():
                if self._distance(graph, cluster_member_graph) > threshold:
                    is_cluster_member = False
                    break
            return is_cluster_member

        while len(s) > 0:
            median_graph: int = self.median_graph(s)
            print(f"median graph: {len(s)}")

            prototype_index: int = self.farthest(s, median_graph)
            prototype_graph: Graph = s[prototype_index]

            cluster = Cluster()
            cluster.set_centroid(prototype_graph)

            iterations: int = 0

            while True:
                with pool.Pool() as executor:
                    futures = [(graph, prototype_graph, self._threshold) for graph in s if
                               graph.get_path() != prototype_graph.get_path()]
                    is_cluster_members = list(executor.map(process_graph, *zip(*futures)))

                for i, graph in enumerate(s):
                    if is_cluster_members[i]:
                        cluster.add_graph(graph)

                cluster_graphs: List[Graph] = cluster.get_graphs()

                new_prototype_index: int = self.median_graph(cluster_graphs)
                new_prototype_graph = cluster_graphs[new_prototype_index]

                iterations += 1

                if new_prototype_graph.get_path() == prototype_graph.get_path() or iterations >= max_iter:
                    self._centroids.append(prototype_graph)
                    print(f"new centroid... {cluster.size()} elements on {iterations} iterations")
                    s = [g for g in s if g.get_path() not in {u.get_path() for u in cluster_graphs}]
                    break

                prototype_graph = new_prototype_graph
                cluster = Cluster()
                cluster.set_centroid(prototype_graph)

    def get_centroids(
            self
    ) -> List[Graph]:
        return self._centroids

    def save_centroids(
            self,
            dir_path: str,
            filename: str
    ) -> None:
        dump_centroids(self.get_centroids(), dir_path + "/" + filename)

    def load_centroids(
            self,
            dir_path: str,
            filename: str
    ) -> None:
        self._centroids = load_centroids(dir_path, filename)

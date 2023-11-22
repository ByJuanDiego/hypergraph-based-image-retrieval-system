from concurrent.futures import ThreadPoolExecutor
import pickle

from typing import Set, Callable, List, Dict, Tuple
from graph.essential import Graph, Cluster


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
            if (g1.get_path(), g2.get_path()) in self._distances_cache:
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

        with ThreadPoolExecutor() as executor:
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
            self
    ) -> None:
        s: List[Graph] = self._graphs.copy()
        self._centroids.clear()

        while len(s) > 0:
            median_graph: int = self.median_graph(s)
            print(f"median graph: {len(s)}")

            prototype_index: int = self.farthest(s, median_graph)
            prototype_graph: Graph = s[prototype_index]

            cluster = Cluster()
            cluster.set_centroid(prototype_graph)

            while True:
                for graph in s:
                    if graph.get_path() == prototype_graph.get_path():
                        continue

                    is_cluster_member = True

                    for cluster_member_graph in cluster.get_graphs():
                        if self._distance(graph, cluster_member_graph) > self._threshold:
                            is_cluster_member = False
                            break

                    if is_cluster_member:
                        cluster.add_graph(graph)

                cluster_entries: List[Graph] = cluster.get_graphs()
                cluster_paths: Set[str] = {g.get_path() for g in cluster_entries}

                new_prototype_index: int = self.median_graph(cluster_entries)
                new_prototype_graph = cluster_entries[new_prototype_index]

                if new_prototype_graph.get_path() == prototype_graph.get_path():
                    self._centroids.append(prototype_graph)
                    print(f"new centroid... {cluster.size()}")
                    s = [g for g in s if g.get_path() not in cluster_paths]
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
        with open(dir_path + "/" + filename, "wb") as file:
            pickle.dump(self.get_centroids(), file)

    def load_centroids(
            self,
            dir_path: str,
            filename: str
    ) -> None:
        with open(dir_path + "/" + filename, "rb") as file:
            self._centroids = pickle.load(file)

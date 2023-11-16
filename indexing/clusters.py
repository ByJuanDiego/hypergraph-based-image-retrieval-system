import sys


class Cluster:
    _centroid: tuple | None = None
    _graphs: list[tuple]

    def __init__(self):
        self._centroid = None
        self._graphs = []

    def clear(self):
        self._graphs.clear()
        self._centroid = None

    def set_centroid(self, graph: tuple):
        self._centroid = graph[1]
        self._graphs = [graph]

    def add_entry(self, entry: tuple):
        self._graphs.append(entry)

    def get_graphs(self):
        return self._graphs

    def size(self):
        return len(self._graphs)


class MeanShift:
    _threshold: float = 0
    _clusters: list[str] = []
    _graphs: dict = {}
    _distance = None

    def __init__(self, graphs: dict, distance_function, threshold: float):
        self._threshold = threshold
        self._clusters = []
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

    def fit(self):
        s = list(self._graphs.items())
        clusters = []

        while len(s) > 0:
            median_graph: int = self.median_graph(s)
            farthest: int = self.farthest(s, median_graph)

            prototype: int = self.farthest(s, farthest)
            prototype_path, prototype_graph = s[prototype]

            cluster = Cluster()
            cluster.set_centroid((prototype_path, prototype_graph))

            while True:
                for path, graph in s:
                    if prototype_path == path:
                        continue

                    is_cluster_member = True

                    for cluster_member_path, cluster_member_graph in cluster.get_graphs():
                        if self._distance(cluster_member_graph, graph) > self._threshold:
                            is_cluster_member = False
                            break

                    if is_cluster_member:
                        cluster.add_entry((path, graph))

                cluster_entries: list[tuple] = cluster.get_graphs()
                cluster_paths: set = {g[0] for g in cluster_entries}

                new_prototype: int = self.median_graph(cluster_entries)
                new_prototype_path, new_prototype_graph = cluster_entries[new_prototype]

                if new_prototype_path == prototype_path:
                    clusters.append(prototype_path)
                    s = [g for g in s if g[0] not in cluster_paths]
                else:
                    cluster = Cluster()
                    cluster.set_centroid((new_prototype_path, new_prototype_graph))

        self._clusters = clusters

    def clusters(self):
        if not self._clusters:
            raise AttributeError("The clusters are empty!")
        return self._clusters

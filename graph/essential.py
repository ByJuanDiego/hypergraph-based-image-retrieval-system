from typing import List, Tuple, Union


class Graph:
    _path: str
    _vertexes: List[Tuple[float, float, float, float]]
    _edges: List[Tuple[int, int]]

    def __init__(self, path: str, vertexes: List[Tuple[float, float, float, float]], edges: List[Tuple[int, int]]):
        self._vertexes = vertexes.copy()
        self._edges = edges.copy()
        self._path = path

    def __repr__(self):
        return f"Path: {self._path}\nVertexes: {self._vertexes}\nEdges: {self._edges}\n"

    def add_vertex(self, vertex: Tuple[float, float, float, float]):
        self._vertexes.append(vertex)

    def add_edge(self, edges: Tuple[int, int]):
        self._edges.append(edges)

    def set_vertexes(self, vertexes: List[Tuple[float, float, float, float]]):
        self._vertexes = vertexes

    def set_edges(self, edges: List[Tuple[int, int]]):
        self._edges = edges

    def get_path(self):
        return self._path

    def get_vertexes(self):
        return self._vertexes

    def get_edges(self):
        return self._edges

    def get_vertex(self, index: int):
        return self._vertexes[index]

    def get_edge(self, index: int):
        return self._edges[index]

    @property
    def vertexes_count(self):
        return len(self._vertexes)

    @property
    def edges_count(self):
        return len(self._edges)


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

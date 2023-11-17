from typing import List, Tuple


class Graph:
    _path: str
    _vertexes: List[Tuple[float, float, float, float]]
    _edges: List[Tuple[int, int]]

    def __init__(self, path: str, vertexes: List[Tuple[float, float, float, float]], edges: List[Tuple[int, int]]):
        self._vertexes = vertexes.copy()
        self._edges = edges.copy()
        self._path = path

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

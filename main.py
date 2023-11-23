from dataset.pickle import load_dataset_in_batches
from graph.essential import Graph
from graph.distances import cosine_score

from retrieval.algorithms import KNN
from indexing.indexes import HyperGraph

from typing import List

from random import choice

graphs: List[Graph] = load_dataset_in_batches("pickles/graphs")


hyper_graph = HyperGraph(graphs=graphs, distance=cosine_score, threshold=7.0, centroids=[])
hyper_graph.load_clusters("pickles/hyper_graphs", "cosine_7.p")
hyper_graph.pretty_print(0)

knn = KNN(hyper_graph)

q: Graph = choice(graphs)
print(f"Query: {q.get_path()}")

retrieval: List[str] = knn.query(q, 5)

for path in retrieval:
    print(path)

from dataset.pickle import load_dataset_in_batches
from graph.essential import Graph
from graph.distances import cosine_score, euclidean_distance, manhattan_distance, weighted_distance

from retrieval.algorithms import knn_retrieval
from indexing.indexes import HyperGraph

from typing import List

from random import choice

graphs: List[Graph] = load_dataset_in_batches("pickles/graphs")


cosine_hyper_graph = HyperGraph(graphs=graphs, distance=cosine_score, threshold=7.0, centroids=[])
cosine_hyper_graph.load_clusters("pickles/hyper_graphs", "cosine_7.p")

euclidean_hyper_graph = HyperGraph(graphs=graphs, distance=euclidean_distance, threshold=7.0, centroids=[])
euclidean_hyper_graph.load_clusters("pickles/hyper_graphs", "euclidean_7.p")

manhattan_hyper_graph = HyperGraph(graphs=graphs, distance=manhattan_distance, threshold=7.0, centroids=[])
manhattan_hyper_graph.load_clusters("pickles/hyper_graphs", "manhattan_7.p")

weighted_hyper_graph = HyperGraph(graphs=graphs, distance=weighted_distance, threshold=7.0, centroids=[])
weighted_hyper_graph.load_clusters("pickles/hyper_graphs", "weighted_7.p")

models: List[HyperGraph] = [
    cosine_hyper_graph,
    euclidean_hyper_graph,
    manhattan_hyper_graph,
    weighted_hyper_graph
]

query = choice(graphs)
print(f"Query: {query.get_path()}\n")

for model in models:
    print(knn_retrieval(model, query, 4))

print()
[model.pretty_print(0) for model in models]

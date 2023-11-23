from typing import List, Dict, Tuple

from dataset.pickle import load_dataset_in_batches, load_graph_distances, load_centroids

from graph.essential import Graph
from graph.distances import weighted_distance, cosine_score, euclidean_distance

from indexing.indexes import HyperGraph


graphs: List[Graph] = load_dataset_in_batches("pickles/graphs")
centroids: List[Graph] = load_centroids("pickles/centroids", "cosine_7.p")

hypergraph = HyperGraph(graphs, centroids, cosine_score, threshold=7.0)
hypergraph.fit()
hypergraph.save_clusters("pickles/hyper_graphs", "cosine_7.p")

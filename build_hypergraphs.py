from typing import List

from dataset.pickle import load_dataset_in_batches, load_centroids

from graph.essential import Graph
from graph.distances import weighted_distance, cosine_score, euclidean_distance, manhattan_distance

from indexing.indexes import HyperGraph


graphs: List[Graph] = load_dataset_in_batches("pickles/graphs")

cosine_centroids: List[Graph] = load_centroids("pickles/centroids", "cosine_6.p")
euclidean_centroids: List[Graph] = load_centroids("pickles/centroids", "euclidean_6.p")
weighted_centroids: List[Graph] = load_centroids("pickles/centroids", "weighted_6.p")
manhattan_centroids: List[Graph] = load_centroids("pickles/centroids", "manhattan_6.p")


def build_hyper_graphs(centroids, distance_fn, save_clusters_path, filename, threshold):
    hypergraph = HyperGraph(graphs, distance_fn, threshold, centroids)

    print("------------------------- start -------------------------")
    hypergraph.fit()
    hypergraph.save_clusters(save_clusters_path, filename)
    hypergraph.pretty_print(0)
    print("-------------------------- end --------------------------")


save_path = "pickles/hyper_graphs"
T = 6.0

print("------------- euclidean distance -------------")
build_hyper_graphs(euclidean_centroids, euclidean_distance, save_path, "euclidean_6.p", T)

print("--------------- cosine distance --------------")
build_hyper_graphs(cosine_centroids, cosine_score, save_path, "cosine_6.p", T)

print("------------- manhattan distance -------------")
build_hyper_graphs(manhattan_centroids, manhattan_distance, save_path, "manhattan_6.p", T)

print("-------------- weighted distance -------------")
build_hyper_graphs(weighted_centroids, weighted_distance, save_path, "weighted_6.p", T)

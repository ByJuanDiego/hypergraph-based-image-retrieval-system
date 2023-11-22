from typing import List, Dict, Tuple

from dataset.pickle import load_dataset_in_batches, load_graph_distances

from graph.essential import Graph
from graph.distances import weighted_distance, cosine_score, euclidean_distance

from indexing.algorithms import MeanShift

graphs: List[Graph] = load_dataset_in_batches("pickles/graphs")

cosine_cache: Dict[Tuple[str, str], float] = load_graph_distances("pickles/distance_cache", "cosine.p")
euclidean_cache: Dict[Tuple[str, str], float] = load_graph_distances("pickles/distance_cache", "euclidean.p")
weighted_cache: Dict[Tuple[str, str], float] = load_graph_distances("pickles/distance_cache", "weighted_distance.p")


def build_centroids(distance_fn, save_centroids_path, filename, threshold, cache):
    mean_shift = MeanShift(graphs=graphs,
                           threshold=threshold,
                           distance_function=distance_fn,
                           distance_cache=cache)

    print("start...")
    mean_shift.fit()
    mean_shift.save_centroids(save_centroids_path, filename)
    print("end.")


save_path = "pickles/centroids"

build_centroids(euclidean_distance, save_path, "euclidean_5.p", 5.0, euclidean_cache)
build_centroids(euclidean_distance, save_path, "euclidean_6.p", 6.0, euclidean_cache)
build_centroids(euclidean_distance, save_path, "euclidean_7.p", 7.0, euclidean_cache)

build_centroids(cosine_score, save_path, "cosine_5.p", 5.0, cosine_cache)
build_centroids(cosine_score, save_path, "cosine_6.p", 6.0, cosine_cache)
build_centroids(cosine_score, save_path, "cosine_7.p", 7.0, cosine_cache)

build_centroids(weighted_distance, save_path, "weighted_5.p", 5.0, weighted_cache)
build_centroids(weighted_distance, save_path, "weighted_6.p", 6.0, weighted_cache)
build_centroids(weighted_distance, save_path, "weighted_7.p", 7.0, weighted_cache)

from typing import List, Dict, Tuple

from dataset.pickle import load_dataset_in_batches, load_graph_distances

from graph.essential import Graph
from graph.distances import weighted_distance, euclidean_distance, manhattan_distance, cosine_score

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

    print("------------------------- start -------------------------")
    mean_shift.fit()
    mean_shift.save_centroids(save_centroids_path, filename)
    print("-------------------------- end --------------------------")


save_path = "pickles/centroids"
T = 6.0

print("------------- euclidean distance -------------")
build_centroids(euclidean_distance, save_path, "euclidean_7.p", T, euclidean_cache)

print("--------------- cosine distance --------------")
build_centroids(cosine_score, save_path, "cosine_7.p", T, cosine_cache)

print("------------- manhattan distance -------------")
build_centroids(manhattan_distance, save_path, "manhattan_6.p", T, cache=None)

print("-------------- weighted distance -------------")
build_centroids(weighted_distance, save_path, "weighted_6.p", T, weighted_cache)

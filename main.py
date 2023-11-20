from typing import List
from dataset.pickle import load_dataset_in_batches
from graph.distances import weighted_distance
from graph.essential import Graph
from indexing.indexes import HyperGraph
from indexing.algorithms import MeanShift

graphs: List[Graph] = load_dataset_in_batches("pickles/graphs")

threshold = 20

# mean_shift = MeanShift(graphs, weighted_distance, threshold)

# mean_shift.fit()
# mean_shift.save_centroids("pickles/20", "centroids.p")

# mean_shift.load_centroids("pickles/20", "centroids.p")
# centroids = mean_shift.get_centroids()

# hypergraph = HyperGraph(graphs, centroids, weighted_distance, threshold)
# hypergraph.fit()
# hypergraph.save_clusters("pickles/20", "clusters.p")
#
# hypergraph.pretty_print()


hypergraph = HyperGraph(graphs, centroids=[], distance=weighted_distance, threshold=threshold)
hypergraph.load_clusters("pickles/20", "clusters.p")
# hypergraph.save_clusters("pickles/20", "clusters.p")
# hypergraph.load_clusters("pickles/20", "clusters.p")

hypergraph.pretty_print()

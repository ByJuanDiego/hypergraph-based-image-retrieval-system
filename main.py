from dataset.pickle import load_dataset_in_batches
from graph.distances import euclidean_distance
from indexing.indexes import HyperGraph
from indexing.algorithms import MeanShift


graphs = load_dataset_in_batches("pickles/graphs")

threshold = 10.0

mean_shift = MeanShift(graphs, euclidean_distance, threshold)
mean_shift.fit()
mean_shift.save_centroids("pickles", "centroids.p")

centroids = mean_shift.get_centroids()

hypergraph = HyperGraph(graphs, centroids, euclidean_distance, threshold)
hypergraph.fit()
hypergraph.save_clusters("pickles", "clusters.p")

hypergraph.pretty_print()

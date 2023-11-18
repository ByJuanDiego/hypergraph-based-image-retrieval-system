from dataset.pickle import load_dataset_in_batches
from graph.distances import euclidean_distance
from indexing.indexes import HyperGraph
from indexing.algorithms import MeanShift


graphs = load_dataset_in_batches("pickles/graphs")

threshold = 7.0

mean_shift = MeanShift(graphs, euclidean_distance, threshold)
mean_shift.fit()
mean_shift.save_centroids("pickles/7", "centroids.p")

centroids = mean_shift.get_centroids()

hypergraph = HyperGraph(graphs, centroids, euclidean_distance, threshold)
hypergraph.fit()
hypergraph.save_clusters("pickles/7", "clusters.p")

hypergraph.pretty_print()

# hypergraph = HyperGraph(graphs, centroids=[], distance=euclidean_distance, threshold=threshold)
# hypergraph.load_clusters("pickles/8", "clusters.p")
# hypergraph.pretty_print()

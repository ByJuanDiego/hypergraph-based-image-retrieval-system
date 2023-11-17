from indexing.clustering import MeanShift
from graph.distances import euclidean
from graph.dataset.pickle import load_graphs

graphs: dict = load_graphs("pickles/graphs.p")

threshold = 10.0
mean_shift = MeanShift(graphs=graphs, distance_function=euclidean, threshold=threshold)

# mean_shift.fit_centroids()
# mean_shift.save_centroids("pickles/centroids.p")

mean_shift.load_centroids("pickles/centroids.p")

# mean_shift.fit_clusters()
# mean_shift.save_clusters("pickles/clusters.p")

mean_shift.load_clusters("pickles/clusters.p")
mean_shift.pretty_print()

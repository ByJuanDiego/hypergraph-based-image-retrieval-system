from indexing.clustering import MeanShift
from graph.distances import euclidean
from graph.dataset.pickle import load_graphs

graphs: dict = load_graphs("pickles/graphs.p")

threshold = 10.0
mean_shift = MeanShift(graphs=graphs, distance_function=euclidean, threshold=threshold)
mean_shift.fit()
mean_shift.save("pickles/centroids.p")
centroids = mean_shift.centroids()
print(centroids)

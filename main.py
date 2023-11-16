from graph.dataset.pickle import load_graphs
from graph.distances import euclidean
from indexing.clusters import MeanShift

graphs: dict = load_graphs("embeddings/graphs_pickled.p")

mean_shift = MeanShift(graphs=graphs, distance_function=euclidean, threshold=10.0)
mean_shift.fit()
clusters = mean_shift.clusters()
print(clusters)

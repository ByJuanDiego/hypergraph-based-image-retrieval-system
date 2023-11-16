from graph.dataset.pickle import load_graphs
from graph.distances import euclidean

graphs = load_graphs("embeddings/graphs_pickled.p")
print(len(graphs))
g1 = graphs["021541071.jpg"]
g2 = graphs["025246930.jpg"]

print(g1)
print(euclidean(g1, g2))

from interface.gui import GUI
from graph.distances import weighted_distance
from indexing.indexes import HyperGraph

hyper_graph = HyperGraph(distance=weighted_distance, threshold=7.0, centroids=[], graphs=[])
hyper_graph.load_clusters("pickles/hyper_graphs", "weighted_7.p")

user_interface = GUI(hyper_graph)
user_interface.run()

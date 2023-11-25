from interface.gui import GUI
from graph.distances import weighted_distance, cosine_score, manhattan_distance, euclidean_distance
from indexing.indexes import HyperGraph

weighted_hyper_graph = HyperGraph(distance=weighted_distance, threshold=7.0, centroids=[], graphs=[])
weighted_hyper_graph.load_clusters("pickles/hyper_graphs", "weighted_7.p")

cosine_hyper_graph = HyperGraph(distance=cosine_score, threshold=7.0, centroids=[], graphs=[])
cosine_hyper_graph.load_clusters("pickles/hyper_graphs", "cosine_7.p")

manhattan_hyper_graph = HyperGraph(distance=manhattan_distance, threshold=7.0, centroids=[], graphs=[])
manhattan_hyper_graph.load_clusters("pickles/hyper_graphs", "manhattan_7.p")

euclidean_hyper_graph = HyperGraph(distance=euclidean_distance, threshold=7.0, centroids=[], graphs=[])
euclidean_hyper_graph.load_clusters("pickles/hyper_graphs", "euclidean_7.p")

user_interface = GUI(
    [
        weighted_hyper_graph,
        manhattan_hyper_graph,
        euclidean_hyper_graph,
        cosine_hyper_graph
    ],
    [
        "weighted distance",
        "manhattan distance",
        "euclidean distance",
        "cosine score"
    ]
)

user_interface.run()

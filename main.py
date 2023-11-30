from interface.gui import GUI
from graph.distances import weighted_distance, cosine_score, manhattan_distance, euclidean_distance
from indexing.indexes import HyperGraph

T = 6.0

weighted_hyper_graph = HyperGraph(distance=weighted_distance, threshold=T, centroids=[], graphs=[])
weighted_hyper_graph.load_clusters("pickles/hyper_graphs", "weighted_6.p")

cosine_hyper_graph = HyperGraph(distance=cosine_score, threshold=T, centroids=[], graphs=[])
cosine_hyper_graph.load_clusters("pickles/hyper_graphs", "cosine_6.p")

manhattan_hyper_graph = HyperGraph(distance=manhattan_distance, threshold=T, centroids=[], graphs=[])
manhattan_hyper_graph.load_clusters("pickles/hyper_graphs", "manhattan_6.p")

euclidean_hyper_graph = HyperGraph(distance=euclidean_distance, threshold=T, centroids=[], graphs=[])
euclidean_hyper_graph.load_clusters("pickles/hyper_graphs", "euclidean_6.p")

user_interface = GUI(
    [
        weighted_hyper_graph,
        cosine_hyper_graph,
        manhattan_hyper_graph,
        euclidean_hyper_graph
    ],
    [
        "weighted distance",
        "cosine score",
        "manhattan distance",
        "euclidean distance"
    ]
)

user_interface.run()

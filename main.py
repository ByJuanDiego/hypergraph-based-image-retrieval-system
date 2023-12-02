from interface.gui import GUI
from graph.distances import weighted_distance, cosine_score, manhattan_distance, euclidean_distance, best_of_the_best_distance, cosine_v_distance, l2__distance
from indexing.indexes import HyperGraph

T = 6

weighted_hyper_graph = HyperGraph(distance=weighted_distance, threshold=T, centroids=[], graphs=[])
weighted_hyper_graph.load_clusters("pickles/hyper_graphs", "weighted_6.p")

cosine_hyper_graph = HyperGraph(distance=cosine_score, threshold=T, centroids=[], graphs=[])
cosine_hyper_graph.load_clusters("pickles/hyper_graphs", "cosine_6.p")

manhattan_hyper_graph = HyperGraph(distance=manhattan_distance, threshold=T, centroids=[], graphs=[])
manhattan_hyper_graph.load_clusters("pickles/hyper_graphs", "manhattan_6.p")

euclidean_hyper_graph = HyperGraph(distance=euclidean_distance, threshold=T, centroids=[], graphs=[])
euclidean_hyper_graph.load_clusters("pickles/hyper_graphs", "euclidean_6.p")

l2_hyper_graph = HyperGraph(distance=l2__distance, threshold=1.5, centroids=[], graphs=[])
l2_hyper_graph.load_clusters("pickles/hyper_graphs", "l2_6.p")

cosine_v_hyper_graph = HyperGraph(distance=cosine_v_distance, threshold=0.055, centroids=[], graphs=[])
cosine_v_hyper_graph.load_clusters("pickles/hyper_graphs", "cosine_v_0_3.p")

best_hyper_graph = HyperGraph(distance=best_of_the_best_distance, threshold=10, centroids=[], graphs=[])
best_hyper_graph.load_clusters("pickles/hyper_graphs", "best_distance_1.5.p")

user_interface = GUI(
    [
        weighted_hyper_graph,
        cosine_hyper_graph,
        manhattan_hyper_graph,
        euclidean_hyper_graph,
        best_hyper_graph,
        cosine_v_hyper_graph,
        l2_hyper_graph
    ],
    [
        "weighted distance",
        "cosine score",
        "manhattan distance",
        "euclidean distance",
        "body distance",
        "cosine v distance",
        "l2 v distance"
    ]
)

user_interface.run()

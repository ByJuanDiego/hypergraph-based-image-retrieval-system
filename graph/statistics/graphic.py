from graph.essential import Graph
from typing import List, Callable
import matplotlib.pyplot as plt
import pickle

def save_graph_distances(
    graphs: List[Graph],
    distance: Callable [[Graph, Graph], float],
    distances_pickle_path: str = "pickles/distances/weighted_distance.p"
) -> None:
    distances:List[float] = []
    for first_graph_index in range(len(graphs)):
            for second_graph_index in range(first_graph_index+1, len(graphs)): 
                distances.append(distance(graphs[first_graph_index], graphs[second_graph_index]))
    with open(distances_pickle_path, "wb") as distances_pickle_file:
        pickle.dump(distances, distances_pickle_file)
    
def load_graph_distances(
    distances_pickle_path: str = "pickles/distances/weighted_distance.p"
) -> List[float]:
    with open(distances_pickle_path, "rb") as distances_pickle_file:
        return pickle.load(distances_pickle_file)

def graph_distances(
    distances:List[float]
) -> None:
    # the histogram of the data
    plt.hist(distances)
    # Boxplot
    # plt.boxplot(distances)
    plt.show()
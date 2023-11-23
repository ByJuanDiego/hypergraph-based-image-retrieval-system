import pickle
import time
import os

from typing import List, Dict, Callable, Tuple

from graph.essential import Graph
from graph.embeddings.full_body_3D import get_graph_from_full_body_image, get_pose_model


def dump_graphs(
        graphs: List[Graph], filename: str
) -> None:
    with open(filename, 'wb') as pickle_file:
        pickle.dump(graphs, pickle_file)


def dump_dataset_in_batches(
        dataset_dir: str,
        pickle_dir: str,
        graphs_per_batch: int,
        threshold: float = 0.8,
        delay: float = 0.05
) -> None:
    pose_model = get_pose_model()

    graphs: List[Graph] = []
    paths: List[str] = os.listdir(dataset_dir)

    current_batch_id: int = 1

    for image_path in paths:

        try:
            total_path: str = dataset_dir + "/" + image_path

            graph: Graph = get_graph_from_full_body_image(path=total_path, pose_model=pose_model, threshold=threshold)
            graphs.append(graph)

        except AttributeError as e:
            print(e)
            continue

        except AssertionError as e:
            print(e)
            continue

        finally:
            time.sleep(delay)

            # dump the graphs collection just when a determined limit was exceeded
            if len(graphs) > graphs_per_batch:
                dump_graphs(graphs=graphs, filename=f"{pickle_dir}/graphs_{current_batch_id}.p")
                graphs = []
                current_batch_id += 1

    # dump the remaining data
    dump_graphs(graphs, f"{pickle_dir}/graphs_{current_batch_id}.p")


def dump_graph_distances(
        graphs: List[Graph],
        distance: Callable[[Graph, Graph], float],
        pickle_dir: str,
        pickle_filename: str
) -> None:
    distances: Dict[Tuple[str, str], float] = {}
    n: int = len(graphs)

    for i in range(n):
        for j in range(i + 1, n):
            d = distance(graphs[i], graphs[j])

            distances[(graphs[i].get_path(), graphs[j].get_path())] = d
            distances[(graphs[j].get_path(), graphs[i].get_path())] = d

    with open(pickle_dir + "/" + pickle_filename, "wb") as file:
        pickle.dump(distances, file)


def dump_centroids(
        graphs: List[Graph], filename: str
) -> None:
    with open(filename, 'wb') as pickle_file:
        pickle.dump(graphs, pickle_file)


def load_graphs(
        filename: str
) -> List[Graph]:
    with open(filename, 'rb') as pickle_file:
        graphs = pickle.load(pickle_file)
        return graphs


def load_dataset_in_batches(
        pickle_dir: str
) -> List[Graph]:
    graphs: List[Graph] = []
    paths = os.listdir(pickle_dir)

    for path in paths:
        graphs += load_graphs(pickle_dir + "/" + path)

    return graphs


def load_graph_distances(
        pickle_dir: str,
        pickle_filename: str
) -> Dict[Tuple[str, str], float]:
    with open(pickle_dir + "/" + pickle_filename, "rb") as file:
        return pickle.load(file)


def load_centroids(
        dir_path: str,
        filename: str
) -> List[Graph]:
    with open(dir_path + "/" + filename, "rb") as file:
        return pickle.load(file)

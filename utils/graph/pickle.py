import pickle
import time
import os

from utils.graph.get import get_graph_from_full_body_image
from utils.graph.feature_models import pose_model


def dump_graphs(graph: dict, filename: str):
    with open(filename, 'wb') as pickle_file:
        pickle.dump(graph, pickle_file)


def load_graphs(filename: str):
    with open(filename, 'rb') as pickle_file:
        graphs = pickle.load(pickle_file)
        return graphs


def pickle_graphs(
        dataset_path: str,
        pickle_path: str,
        graphs_per_batch: int,
        threshold: float = 0.8,
        delay: float = 0.5
):
    graphs = {}
    paths = os.listdir(dataset_path)

    current_batch_id = 1
    i = 0

    for image_path in paths:

        try:
            total_path = dataset_path + "/" + image_path

            vertexes, edges = get_graph_from_full_body_image(path=total_path, model=pose_model, threshold=threshold)
            graphs[image_path] = (vertexes, edges)

        except AttributeError as e:
            print(e)
            continue

        except AssertionError as e:
            print(e)
            continue

        finally:
            if i % 10 == 0:
                time.sleep(delay)

            # dump the graph collection just when a determined limit was exceeded
            current_batch_size = len(graphs)

            if current_batch_size > graphs_per_batch:
                dump_graphs(graphs, f"{pickle_path}/graphs_{current_batch_id}.p")
                graphs = {}
                current_batch_id += 1

    # dump the remaining data
    dump_graphs(graphs, f"{pickle_path}/graphs_{current_batch_id}.p")

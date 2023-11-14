import os
import time
import pickle
import subprocess

from helpers.get_graph_from_full_body_image import get_graph


DATASET_PATH = "images"
NEW_PATH = "filtered_images"

paths = os.listdir(DATASET_PATH)

processed_images = 0

graphs = {}


for image_path in paths:

    try:
        total_path = DATASET_PATH + "/" + image_path
        new_total_path = NEW_PATH + "/" + image_path

        V, E = get_graph(path=total_path, threshold=0.85)
        subprocess.run(["cp", total_path, new_total_path])

        graphs[image_path] = (V, E)
        processed_images += 1

    except AssertionError:
        continue

    finally:

        if processed_images % 100 == 0:
            print("a:", processed_images)

        time.sleep(1)

        # si demasiados grafos en ram, botalos
        if len(graphs) > 5000:
            with open(f"embeddings/graphs_pickled_{processed_images}.p", 'wb') as pickle_file:
                pickle.dump(graphs, pickle_file)
            graphs = {}


# bota los sobrantes a un ultimo archivo
with open(f"embeddings/graphs_pickled_{processed_images}.p", 'wb') as pickle_file:
    pickle.dump(graphs, pickle_file)

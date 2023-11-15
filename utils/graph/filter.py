import subprocess
import time
import os

from utils.graph.get import get_graph_from_full_body_image
from utils.graph.feature_models import pose_model


def filter_dataset(
        dataset_path: str,
        new_dataset_path: str,
        threshold: float = 0.8,
        delay: float = 0.5
):
    paths = os.listdir(dataset_path)
    i = 0

    for image_path in paths:
        i += 1

        try:
            total_path = dataset_path + "/" + image_path
            _, _ = get_graph_from_full_body_image(path=total_path, model=pose_model, threshold=threshold)

            new_total_path = new_dataset_path + "/" + image_path
            subprocess.run(["cp", total_path, new_total_path])

        except AttributeError:
            continue

        except AssertionError:
            continue

        finally:
            if i % 10 == 0:
                time.sleep(delay)

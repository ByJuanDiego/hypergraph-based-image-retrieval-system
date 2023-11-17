import subprocess
import time
import os

from graph.embeddings.full_body_3D import get_graph_from_full_body_image
from graph.embeddings.full_body_3D import get_pose_model


def filter_dataset(
        dataset_dir: str,
        new_dataset_dir: str,
        threshold: float = 0.8,
        delay: float = 0.5
):
    pose_model = get_pose_model()
    paths = os.listdir(dataset_dir)
    i = 0

    for image_path in paths:
        i += 1

        try:
            total_path = dataset_dir + "/" + image_path
            _ = get_graph_from_full_body_image(path=total_path, pose_model=pose_model, threshold=threshold)

            new_total_path = new_dataset_dir + "/" + image_path
            subprocess.run(["cp", total_path, new_total_path])

        except AttributeError:
            continue

        except AssertionError:
            continue

        finally:
            if i % 10 == 0:
                time.sleep(delay)

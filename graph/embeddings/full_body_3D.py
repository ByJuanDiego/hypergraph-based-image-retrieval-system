import mediapipe as mp
import cv2

from graph.essential import Graph


def get_pose_model(
) -> mp.solutions.pose.Pose:
    return mp.solutions.pose.Pose(
        static_image_mode=True,
        model_complexity=2
    )


def get_graph_from_full_body_image(
        path: str,
        pose_model: mp.solutions.pose.Pose,
        threshold: float
) -> Graph:
    image = cv2.imread(path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = pose_model.process(image_rgb)

    if results is None:
        raise AttributeError("Empty result")

    nodes = []
    avg = 0

    for data_point in results.pose_landmarks.landmark:
        nodes.append(tuple(
            (data_point.x, data_point.y, data_point.z, data_point.visibility)
        ))
        avg += float(data_point.visibility)

    avg /= len(results.pose_landmarks.landmark)

    if avg < threshold:
        raise AssertionError("The image may contain an invalid person")

    edges = list(mp.solutions.pose.POSE_CONNECTIONS)
    return Graph(path, nodes, edges)

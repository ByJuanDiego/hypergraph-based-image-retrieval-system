import cv2
import mediapipe as mp


def get_graph_from_full_body_image(path: str, model: mp.solutions.pose.SolutionBase, threshold: float):
    image = cv2.imread(path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = model.process(image_rgb)

    if results is None:
        raise AttributeError("Empty result")

    nodes = []
    avg = 0

    for data_point in results.pose_landmarks.landmark:
        nodes.append(tuple(
            (data_point.x, data_point.y, data_point.z)
        ))
        avg += float(data_point.visibility)

    avg /= len(results.pose_landmarks.landmark)

    if avg < threshold:
        raise AssertionError("The image may contain an invalid person")

    edges = list(mp.solutions.pose.POSE_CONNECTIONS)
    return nodes, edges

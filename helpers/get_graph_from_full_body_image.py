import cv2
import mediapipe as mp


def get_graph(path: str, threshold):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2) as holistic:
        image = cv2.imread(path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = holistic.process(image_rgb)
        # print(results.pose_landmarks) => None (verificar)

        # Plot: puntos de referencia y conexiones en matplotlib 3D
        # mp_drawing.plot_landmarks(
        #     results.pose_landmarks, mp_pose.POSE_CONNECTIONS
        # )

        nodes = []
        avg = 0

        for data_point in results.pose_landmarks.landmark:
            nodes.append(tuple(
                (data_point.x, data_point.y, data_point.z)
            ))
            avg += float(data_point.visibility)

        avg /= len(results.pose_landmarks.landmark)

        if avg < threshold:
            raise AssertionError("A")

        edges = list(mp_pose.POSE_CONNECTIONS)
        return nodes, edges

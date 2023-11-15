import mediapipe as mp

pose_model = mp.solutions.pose.Pose(
        static_image_mode=True,
        model_complexity=2
)

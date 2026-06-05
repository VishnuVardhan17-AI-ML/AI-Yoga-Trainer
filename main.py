import cv2
import mediapipe as mp

from app.angle_calculator import calculate_angle

from app.pose_detector import (
    detect_tree_pose,
    detect_warrior_pose,
    detect_chair_pose,
    detect_cobra_pose
)

from app.feedback_engine import get_feedback
from app.timer_engine import update_timer

from app.accuracy_engine import (
    calculate_tree_accuracy,
    calculate_warrior_accuracy,
    calculate_chair_accuracy
)

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose()
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if not success:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    pose_name = "NOT DETECTED"
    feedback = "Keep Practicing"
    accuracy = 0
    timer = 0

    if results.pose_landmarks:

        lm = results.pose_landmarks.landmark

        # LEFT ARM
        left_shoulder = [lm[11].x, lm[11].y]
        left_elbow = [lm[13].x, lm[13].y]
        left_wrist = [lm[15].x, lm[15].y]

        # RIGHT ARM
        right_shoulder = [lm[12].x, lm[12].y]
        right_elbow = [lm[14].x, lm[14].y]
        right_wrist = [lm[16].x, lm[16].y]

        # LEFT LEG
        left_hip = [lm[23].x, lm[23].y]
        left_knee = [lm[25].x, lm[25].y]
        left_ankle = [lm[27].x, lm[27].y]

        # RIGHT LEG
        right_hip = [lm[24].x, lm[24].y]
        right_knee = [lm[26].x, lm[26].y]
        right_ankle = [lm[28].x, lm[28].y]

        # ANGLES
        left_elbow_angle = calculate_angle(
            left_shoulder,
            left_elbow,
            left_wrist
        )

        right_elbow_angle = calculate_angle(
            right_shoulder,
            right_elbow,
            right_wrist
        )

        left_knee_angle = calculate_angle(
            left_hip,
            left_knee,
            left_ankle
        )

        right_knee_angle = calculate_angle(
            right_hip,
            right_knee,
            right_ankle
        )

        # TREE POSE
        pose_name = detect_tree_pose(
            left_knee_angle,
            right_knee_angle
        )

        # WARRIOR POSE
        warrior_pose = detect_warrior_pose(
            left_knee_angle,
            right_knee_angle,
            left_elbow_angle,
            right_elbow_angle
        )

        if warrior_pose:
            pose_name = warrior_pose

        # CHAIR POSE
        chair_pose = detect_chair_pose(
            left_knee_angle,
            right_knee_angle,
            left_elbow_angle,
            right_elbow_angle
        )

        if chair_pose:
            pose_name = chair_pose

        # COBRA POSE
        cobra_pose = detect_cobra_pose(
            left_elbow_angle,
            right_elbow_angle,
            left_knee_angle,
            right_knee_angle
        )

        if cobra_pose:
            pose_name = cobra_pose

        # FEEDBACK
        feedback = get_feedback(pose_name)

        # TIMER
        timer = update_timer(pose_name)

        # ACCURACY
        if pose_name == "TREE POSE":
            accuracy = calculate_tree_accuracy(
                left_knee_angle,
                right_knee_angle
            )

        elif pose_name == "WARRIOR POSE":
            accuracy = calculate_warrior_accuracy(
                left_knee_angle,
                right_knee_angle,
                left_elbow_angle,
                right_elbow_angle
            )

        elif pose_name == "CHAIR POSE":
            accuracy = calculate_chair_accuracy(
                left_knee_angle,
                right_knee_angle,
                left_elbow_angle,
                right_elbow_angle
            )

        # DRAW SKELETON
        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        # POSE NAME
        cv2.putText(
            frame,
            pose_name,
            (250, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            3
        )

        # FEEDBACK
        cv2.putText(
            frame,
            feedback,
            (250, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

        # ACCURACY
        cv2.putText(
            frame,
            f"Accuracy: {accuracy}%",
            (250, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        # TIMER
        cv2.putText(
            frame,
            f"Timer: {timer}s",
            (250, 170),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 255),
            2
        )

        # POSE COMPLETED
        if timer >= 5:
            cv2.putText(
                frame,
                "POSE COMPLETED",
                (250, 210),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                3
            )

        # ANGLES
        cv2.putText(
            frame,
            f"L Elbow: {int(left_elbow_angle)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"R Elbow: {int(right_elbow_angle)}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"L Knee: {int(left_knee_angle)}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"R Knee: {int(right_knee_angle)}",
            (20, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    cv2.imshow("AI Yoga Trainer", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
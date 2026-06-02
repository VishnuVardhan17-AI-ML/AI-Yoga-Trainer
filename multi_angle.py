import cv2
import mediapipe as mp
import numpy as np

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(
        c[1] - b[1],
        c[0] - b[0]
    ) - np.arctan2(
        a[1] - b[1],
        a[0] - b[0]
    )

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle


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

    if results.pose_landmarks:

        lm = results.pose_landmarks.landmark

        # LEFT ARM
        left_shoulder = [lm[11].x, lm[11].y]
        left_elbow = [lm[13].x, lm[13].y]
        left_wrist = [lm[15].x, lm[15].y]

        left_elbow_angle = calculate_angle(
            left_shoulder,
            left_elbow,
            left_wrist
        )

        # RIGHT ARM
        right_shoulder = [lm[12].x, lm[12].y]
        right_elbow = [lm[14].x, lm[14].y]
        right_wrist = [lm[16].x, lm[16].y]

        right_elbow_angle = calculate_angle(
            right_shoulder,
            right_elbow,
            right_wrist
        )

        # LEFT LEG
        left_hip = [lm[23].x, lm[23].y]
        left_knee = [lm[25].x, lm[25].y]
        left_ankle = [lm[27].x, lm[27].y]

        left_knee_angle = calculate_angle(
            left_hip,
            left_knee,
            left_ankle
        )

        # RIGHT LEG
        right_hip = [lm[24].x, lm[24].y]
        right_knee = [lm[26].x, lm[26].y]
        right_ankle = [lm[28].x, lm[28].y]

        right_knee_angle = calculate_angle(
            right_hip,
            right_knee,
            right_ankle
        )

        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        cv2.putText(frame,
                    f"L Elbow: {int(left_elbow_angle)}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2)

        cv2.putText(frame,
                    f"R Elbow: {int(right_elbow_angle)}",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2)

        cv2.putText(frame,
                    f"L Knee: {int(left_knee_angle)}",
                    (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2)

        cv2.putText(frame,
                    f"R Knee: {int(right_knee_angle)}",
                    (20, 160),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2)

    cv2.imshow("Yoga Angle Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# Angles calculate
left_elbow_angle = ...
right_elbow_angle = ...
left_knee_angle = ...
right_knee_angle = ...

# Tree Pose Detection
pose_name = "NOT DETECTED"

if left_knee_angle > 160 and right_knee_angle < 100:
    pose_name = "TREE POSE"

elif right_knee_angle > 160 and left_knee_angle < 100:
    pose_name = "TREE POSE"

# Display
cv2.putText(...)
cv2.imshow(...)
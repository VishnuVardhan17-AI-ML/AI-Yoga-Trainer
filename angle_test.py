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

        shoulder = [
            lm[11].x,
            lm[11].y
        ]

        elbow = [
            lm[13].x,
            lm[13].y
        ]

        wrist = [
            lm[15].x,
            lm[15].y
        ]

        angle = calculate_angle(
            shoulder,
            elbow,
            wrist
        )

        print(
            f"Left Elbow Angle: {angle:.2f}"
        )

    cv2.imshow(
        "Angle Detection",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
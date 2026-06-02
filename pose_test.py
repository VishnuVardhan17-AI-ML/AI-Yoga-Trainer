import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if not success:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = pose.process(rgb)

    if results.pose_landmarks:
        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    cv2.imshow("Yoga AI", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

def detect_warrior_pose(
    left_knee_angle,
    right_knee_angle,
    left_elbow_angle,
    right_elbow_angle
):

    if (
        80 <= left_knee_angle <= 120
        and right_knee_angle > 150
        and left_elbow_angle > 150
        and right_elbow_angle > 150
    ):
        return "WARRIOR POSE"

    if (
        80 <= right_knee_angle <= 120
        and left_knee_angle > 150
        and left_elbow_angle > 150
        and right_elbow_angle > 150
    ):
        return "WARRIOR POSE"

    return None
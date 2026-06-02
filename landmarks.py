import cv2
import mediapipe as mp

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

        landmarks = results.pose_landmarks.landmark

        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]

        left_knee = landmarks[25]
        right_knee = landmarks[26]

        print(
            f"LS=({left_shoulder.x:.2f},{left_shoulder.y:.2f}) | "
            f"RS=({right_shoulder.x:.2f},{right_shoulder.y:.2f})"
        )

        print(
            f"LK=({left_knee.x:.2f},{left_knee.y:.2f}) | "
            f"RK=({right_knee.x:.2f},{right_knee.y:.2f})"
        )

        print("-" * 50)

    cv2.imshow("Landmarks", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import mediapipe as mp
import av

from app.correction_engine import get_pose_correction
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

# 1. PAGE SETUP
st.set_page_config(
    page_title="AI Yoga Trainer Pro",
    page_icon="🧘",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #dbeafe, #ede9fe);
}
h1, h3 {
    color: #1E3A8A !important;
    text-align: center;
}
[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-weight: bold;
}
[data-testid="stMetricLabel"] {
    color: #374151 !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🧘 AI Yoga Trainer Pro")
st.markdown("### Real-Time Yoga Pose Detection using AI & Computer Vision")

# 2. GLOBAL POSE DETECTOR
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

# Thread-safe global initialization
pose_detector = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# 3. STATE INITIALIZATION
if "metrics" not in st.session_state:
    st.session_state.metrics = {"pose": "Waiting", "accuracy": "0%", "timer": "0s"}

# 4. SIDEBAR
st.sidebar.title("🧘 Control Panel")
st.sidebar.success("Camera Active")
st.sidebar.markdown("""
### Supported Poses
✅ Tree Pose
✅ Warrior Pose
✅ Chair Pose
✅ Cobra Pose
""")
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Pose Counter")

tree_cnt = st.sidebar.empty()
warrior_cnt = st.sidebar.empty()
chair_cnt = st.sidebar.empty()
cobra_cnt = st.sidebar.empty()

tree_cnt.write("Tree Pose : 0")
warrior_cnt.write("Warrior Pose : 0")
chair_cnt.write("Chair Pose : 0")
cobra_cnt.write("Cobra Pose : 0")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Current Pose", st.session_state.metrics["pose"])
with col2:
    st.metric("Accuracy", st.session_state.metrics["accuracy"])
with col3:
    st.metric("Session Timer", st.session_state.metrics["timer"])
    progress_bar = st.progress(0)

# 5. FRAME CALLBACK
def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    img = frame.to_ndarray(format="bgr24")
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    try:
        results = pose_detector.process(rgb)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark

            left_shoulder  = [lm[11].x, lm[11].y]
            left_elbow     = [lm[13].x, lm[13].y]
            left_wrist     = [lm[15].x, lm[15].y]

            right_shoulder = [lm[12].x, lm[12].y]
            right_elbow    = [lm[14].x, lm[14].y]
            right_wrist    = [lm[16].x, lm[16].y]

            left_hip   = [lm[23].x, lm[23].y]
            left_knee  = [lm[25].x, lm[25].y]
            left_ankle = [lm[27].x, lm[27].y]

            right_hip   = [lm[24].x, lm[24].y]
            right_knee  = [lm[26].x, lm[26].y]
            right_ankle = [lm[28].x, lm[28].y]

            left_elbow_angle  = calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            left_knee_angle   = calculate_angle(left_hip, left_knee, left_ankle)
            right_knee_angle  = calculate_angle(right_hip, right_knee, right_ankle)

            pose_name = "Unknown Pose"

            tree_pose = detect_tree_pose(left_knee_angle, right_knee_angle)
            if tree_pose:
                pose_name = tree_pose

            warrior_pose = detect_warrior_pose(
                left_knee_angle, right_knee_angle, left_elbow_angle, right_elbow_angle
            )
            if warrior_pose:
                pose_name = warrior_pose

            chair_pose = detect_chair_pose(
                left_knee_angle, right_knee_angle, left_elbow_angle, right_elbow_angle
            )
            if chair_pose:
                pose_name = chair_pose

            cobra_pose = detect_cobra_pose(
                left_elbow_angle, right_elbow_angle, left_knee_angle, right_knee_angle
            )
            if cobra_pose:
                pose_name = cobra_pose

            try:
                feedback   = get_feedback(pose_name)
                correction = get_pose_correction(
                    pose_name, left_knee_angle, right_knee_angle,
                    left_elbow_angle, right_elbow_angle
                )
                timer = update_timer(pose_name)
            except Exception as e:
                print(f"ENGINE ERROR: {e}")
                feedback   = "Good"
                correction = ""
                timer      = 0

            accuracy = 0
            if pose_name == "TREE POSE":
                accuracy = calculate_tree_accuracy(left_knee_angle, right_knee_angle)
            elif pose_name == "WARRIOR POSE":
                accuracy = calculate_warrior_accuracy(
                    left_knee_angle, right_knee_angle, left_elbow_angle, right_elbow_angle
                )
            elif pose_name == "CHAIR POSE":
                accuracy = calculate_chair_accuracy(
                    left_knee_angle, right_knee_angle, left_elbow_angle, right_elbow_angle
                )

            mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            cv2.putText(img, pose_name,                (20, 40),  cv2.FONT_HERSHEY_SIMPLEX, 1,   (0, 255, 0),   2)
            cv2.putText(img, f"Accuracy: {accuracy}%", (20, 80),  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(img, f"Feedback: {feedback}",  (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(img, f"Timer: {timer}s",        (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
            
            if correction:
                cv2.putText(img, f"Fix: {correction}", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 128, 255), 2) 
                
            if timer >= 5:
                cv2.putText(img, "POSE COMPLETED!", (150, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)
                cv2.putText(img, pose_name,         (180, 350), cv2.FONT_HERSHEY_SIMPLEX, 1,   (255, 255, 0), 3)

    except Exception as e:
        print(f"FRAME ERROR: {e}")

    return av.VideoFrame.from_ndarray(img, format="bgr24")

# 6. STREAMER
webrtc_streamer(
    key="pose-trainer",
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False}
)

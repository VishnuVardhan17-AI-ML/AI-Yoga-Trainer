import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import mediapipe as mp
import av

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

st.set_page_config(
    page_title="AI Yoga Trainer Pro",
    page_icon="🧘",
    layout="wide"
)
st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #dbeafe,
        #ede9fe
    );
}

h1 {
    color: #1E3A8A !important;
    text-align: center;
}

h3 {
    color: #111827 !important;
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
st.markdown(
    "### Real-Time Yoga Pose Detection using AI & Computer Vision"
)

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

st.sidebar.write("Tree Pose : 0")
st.sidebar.write("Warrior Pose : 0")
st.sidebar.write("Chair Pose : 0")
st.sidebar.write("Cobra Pose : 0")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current Pose", "Waiting")

with col2:
    st.metric("Accuracy", "0%")

with col3:
    st.metric("Session Timer", "0s")
    
    progress_bar = st.progress(0)

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

# Use a persistent instance of the Mediapipe Pose detector
if "pose_detector" not in st.session_state:
    st.session_state.pose_detector = mp_pose.Pose()

def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    img = frame.to_ndarray(format="bgr24")
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    results = st.session_state.pose_detector.process(rgb)
    
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
        left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
        right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
        
        # POSE DETECTION (Initialize fallback name)
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
            
        feedback = get_feedback(pose_name)
        timer = update_timer(pose_name)
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
            
        # DRAW SKELETON
        mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # DISPLAY
        cv2.putText(img, pose_name, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, f"Accuracy: {accuracy}%", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(img, feedback, (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(img, f"Timer: {timer}s", (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        
    return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="pose-trainer",
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False}
)

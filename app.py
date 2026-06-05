import streamlit as st
import time

st.set_page_config(
    page_title="AI Yoga Trainer",
    page_icon="🧘",
    layout="wide"
)

# CUSTOM CSS
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#0f172a,#1e293b);
}

.big-title {
    text-align: center;
    font-size: 60px;
    font-weight: bold;
    color: #38bdf8;
    animation: glow 2s infinite alternate;
}

.subtitle {
    text-align: center;
    color: white;
    font-size: 22px;
}

@keyframes glow {
    from {
        text-shadow: 0 0 10px #38bdf8;
    }
    to {
        text-shadow: 0 0 35px #38bdf8;
    }
}

.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 15px;
    margin-top: 10px;
    color: white;
    box-shadow: 0px 0px 20px rgba(56,189,248,0.3);
}

.pose-box {
    background: #0f766e;
    padding: 15px;
    border-radius: 12px;
    color: white;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
}

.footer {
    text-align:center;
    color:white;
    margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# TITLE
st.markdown(
    '<p class="big-title">🧘 AI Yoga Trainer</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Real-Time Yoga Pose Detection & Feedback System</p>',
    unsafe_allow_html=True
)

st.markdown("---")

# LOADING ANIMATION
st.subheader("🚀 Initializing AI Engine")

progress_bar = st.progress(0)

for i in range(100):
    time.sleep(0.01)
    progress_bar.progress(i + 1)

st.success("AI Yoga Trainer Ready")

st.markdown("---")

# FEATURES + TECH
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
    <h2>✨ Features</h2>

    ✅ Tree Pose Detection<br><br>
    ✅ Warrior Pose Detection<br><br>
    ✅ Chair Pose Detection<br><br>
    ✅ Cobra Pose Detection<br><br>
    ✅ Real-Time Feedback<br><br>
    ✅ Accuracy Engine<br><br>
    ✅ Pose Hold Timer

    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <h2>🛠 Technologies</h2>

    🐍 Python<br><br>
    📸 OpenCV<br><br>
    🤖 MediaPipe<br><br>
    🔢 NumPy<br><br>
    🌐 Streamlit

    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# POSE SELECTOR
st.header("🧘 Supported Yoga Poses")

pose = st.selectbox(
    "Choose a Yoga Pose",
    [
        "Tree Pose",
        "Warrior Pose",
        "Chair Pose",
        "Cobra Pose"
    ]
)

st.markdown(
    f"""
    <div class="pose-box">
    Selected Pose: {pose}
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

if pose == "Tree Pose":
    st.success("Maintain balance on one leg while keeping the other bent.")

elif pose == "Warrior Pose":
    st.success("Keep one knee bent and both arms stretched.")

elif pose == "Chair Pose":
    st.success("Sit back as if sitting on an invisible chair.")

elif pose == "Cobra Pose":
    st.success("Lift your chest upward while keeping legs extended.")

st.markdown("---")

# PROJECT METRICS
st.header("📊 Project Statistics")

m1, m2, m3 = st.columns(3)

with m1:
    st.metric(
        label="Supported Poses",
        value="4"
    )

with m2:
    st.metric(
        label="Feedback Engine",
        value="Active"
    )

with m3:
    st.metric(
        label="Accuracy Engine",
        value="Active"
    )

st.markdown("---")

# FUTURE FEATURES
st.header("🚀 Future Enhancements")

st.info("🔊 Voice Feedback")
st.info("📈 Workout Tracking Dashboard")
st.info("🧘 Additional Yoga Poses")
st.info("🌐 Live Webcam Integration")
st.info("🤖 AI Pose Correction")

st.markdown("---")

# DEVELOPER
st.markdown("""
<div class="footer">
<h3>👨‍💻 Developed By</h3>
<h2>G Vishnu Vardhan</h2>
<p>AI • Machine Learning • Computer Vision</p>
</div>
""", unsafe_allow_html=True)
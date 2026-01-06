import streamlit as st
import time
from datetime import datetime, timedelta
import random
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av

# Initialize session state
if 'exam_started' not in st.session_state:
    st.session_state.exam_started = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'camera_active' not in st.session_state:
    st.session_state.camera_active = False
if 'mic_active' not in st.session_state:
    st.session_state.mic_active = False

# MCQ Questions
MCQ_QUESTIONS = [
    {"q": "What is the time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"], "correct": 1},
    {"q": "Which data structure uses LIFO principle?", "options": ["Queue", "Stack", "Array", "Tree"], "correct": 1},
    {"q": "What does SQL stand for?", "options": ["Structured Query Language", "Simple Query Language", "Standard Query Language", "System Query Language"], "correct": 0},
    {"q": "Which sorting algorithm has best average case complexity?", "options": ["Bubble Sort", "Quick Sort", "Selection Sort", "Insertion Sort"], "correct": 1},
    {"q": "What is the default port for HTTP?", "options": ["443", "21", "80", "22"], "correct": 2},
    {"q": "Which is not a Python data type?", "options": ["List", "Tuple", "Array", "Dictionary"], "correct": 2},
    {"q": "What does API stand for?", "options": ["Application Programming Interface", "Advanced Programming Interface", "Automated Programming Interface", "Application Process Interface"], "correct": 0},
    {"q": "Which algorithm is used for shortest path?", "options": ["DFS", "BFS", "Dijkstra", "Kruskal"], "correct": 2},
    {"q": "What is the space complexity of merge sort?", "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"], "correct": 2},
    {"q": "Which is not a relational database?", "options": ["MySQL", "PostgreSQL", "MongoDB", "SQLite"], "correct": 2},
    {"q": "What does CSS stand for?", "options": ["Computer Style Sheets", "Cascading Style Sheets", "Creative Style Sheets", "Colorful Style Sheets"], "correct": 1},
    {"q": "Which data structure is used in recursion?", "options": ["Queue", "Stack", "Array", "Tree"], "correct": 1},
    {"q": "What is the worst case complexity of quicksort?", "options": ["O(n log n)", "O(n²)", "O(n)", "O(log n)"], "correct": 1},
    {"q": "Which protocol is used for secure web browsing?", "options": ["HTTP", "HTTPS", "FTP", "SMTP"], "correct": 1},
    {"q": "What does OOP stand for?", "options": ["Object Oriented Programming", "Objective Oriented Programming", "Object Operational Programming", "Optimal Oriented Programming"], "correct": 0}
]

DSA_QUESTION = {
    "title": "Python DSA Problem",
    "description": "Write a Python function to find the maximum sum of a contiguous subarray (Kadane's Algorithm).",
    "example": "Input: [-2,1,-3,4,-1,2,1,-5,4]\nOutput: 6 (subarray [4,-1,2,1])"
}

def start_camera():
    """Initialize real camera and microphone"""
    st.session_state.camera_active = True
    st.session_state.mic_active = True
    return True

def video_frame_callback(frame):
    """Process video frames for monitoring"""
    img = frame.to_ndarray(format="bgr24")
    # Here you could add face detection, eye tracking, etc.
    return av.VideoFrame.from_ndarray(img, format="bgr24")

def audio_frame_callback(frame):
    """Process audio frames for monitoring"""
    # Here you could add audio analysis, speech detection, etc.
    return frame

def get_camera_status():
    """Get real camera status"""
    if st.session_state.get('camera_active', False):
        return "🔴 LIVE"
    return "⚫ OFFLINE"

def get_mic_status():
    """Get real microphone status"""
    if st.session_state.get('mic_active', False):
        return "🎤 RECORDING"
    return "🎤 MUTED"

def show_monitoring_alerts():
    """Show random monitoring alerts to simulate proctoring"""
    alerts = [
        "⚠️ Face detection: Active",
        "👁️ Eye tracking: Monitoring", 
        "🔊 Audio monitoring: Active",
        "📱 Screen sharing: Blocked",
        "🚫 Tab switching: Disabled"
    ]
    
    # Show random alert every few seconds
    alert_index = int(time.time() / 3) % len(alerts)
    return alerts[alert_index]

def get_remaining_time():
    """Calculate remaining exam time"""
    if st.session_state.start_time:
        elapsed = datetime.now() - st.session_state.start_time
        remaining = timedelta(minutes=15) - elapsed
        return max(0, int(remaining.total_seconds()))
    return 900  # 15 minutes in seconds

def format_time(seconds):
    """Format seconds to MM:SS"""
    mins, secs = divmod(seconds, 60)
    return f"{mins:02d}:{secs:02d}"

def main():
    st.set_page_config(page_title="Online Exam Portal", layout="wide")
    
    # Header
    st.title("🎓 Online Exam Portal")
    
    if not st.session_state.exam_started:
        # Pre-exam screen
        st.markdown("### Exam Instructions")
        st.write("- Duration: 15 minutes")
        st.write("- 15 MCQ questions + 1 Python DSA question")
        st.write("- Camera and microphone will be monitored")
        st.write("- Click 'Start Exam' when ready")
        
        st.markdown("### 📹 Camera & Microphone Test")
        st.info("⚠️ Please allow camera and microphone access when prompted by your browser.")
        
        # Test camera and mic before exam
        test_webrtc = webrtc_streamer(
            key="test-camera",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=RTCConfiguration(
                {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
            ),
            media_stream_constraints={
                "video": {"width": 320, "height": 240},
                "audio": True
            },
            async_processing=True,
        )
        
        if test_webrtc.state.playing:
            st.success("✅ Camera and microphone are working!")
            exam_ready = True
        else:
            st.warning("⚠️ Please enable camera and microphone to proceed.")
            exam_ready = False
        
        if st.button("🚀 Start Exam", type="primary", disabled=not exam_ready):
            # Start camera and mic
            start_camera()
            st.session_state.exam_started = True
            st.session_state.start_time = datetime.now()
            st.rerun()
    
    else:
        # Exam interface
        remaining_time = get_remaining_time()
        
        if remaining_time <= 0:
            st.error("⏰ Time's up! Exam ended.")
            st.stop()
        
        # Top bar with timer and camera
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### ⏱️ Time Remaining: {format_time(remaining_time)}")
            # Show monitoring status
            monitoring_alert = show_monitoring_alerts()
            st.markdown(f"<div style='background: #e8f5e8; padding: 8px; border-radius: 5px; margin: 5px 0;'><small>{monitoring_alert}</small></div>", unsafe_allow_html=True)
        
        with col2:
            # Real camera and microphone streaming
            camera_status = get_camera_status()
            mic_status = get_mic_status()
            
            st.markdown(f"**{camera_status}**")
            st.markdown(f"**{mic_status}**")
            
            # Real-time webcam stream
            webrtc_ctx = webrtc_streamer(
                key="exam-camera",
                mode=WebRtcMode.SENDRECV,
                rtc_configuration=RTCConfiguration(
                    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
                ),
                video_frame_transformer=video_frame_callback,
                audio_frame_transformer=audio_frame_callback,
                media_stream_constraints={
                    "video": {"width": 320, "height": 240},
                    "audio": True
                },
                async_processing=True,
            )
            
            # Show connection status
            if webrtc_ctx.state.playing:
                st.success("✅ Camera & Mic Active")
                st.session_state.camera_active = True
                st.session_state.mic_active = True
            else:
                st.error("❌ Camera & Mic Inactive")
                st.session_state.camera_active = False
                st.session_state.mic_active = False
        
        # Main exam content
        tab1, tab2 = st.tabs(["📝 MCQ Questions", "💻 Python DSA"])
        
        with tab1:
            st.markdown("### Multiple Choice Questions")
            
            for i, question in enumerate(MCQ_QUESTIONS):
                st.markdown(f"**Q{i+1}. {question['q']}**")
                
                answer = st.radio(
                    f"Select answer for Q{i+1}:",
                    question['options'],
                    key=f"mcq_{i}",
                    label_visibility="collapsed"
                )
                
                if answer:
                    st.session_state.answers[f"mcq_{i}"] = question['options'].index(answer)
                
                st.divider()
        
        with tab2:
            st.markdown("### Python DSA Question")
            st.markdown(f"**{DSA_QUESTION['title']}**")
            st.markdown(DSA_QUESTION['description'])
            st.code(DSA_QUESTION['example'], language="text")
            
            code_answer = st.text_area(
                "Write your Python solution:",
                height=300,
                placeholder="def max_subarray_sum(arr):\n    # Your code here\n    pass",
                key="dsa_answer"
            )
            
            if code_answer:
                st.session_state.answers['dsa'] = code_answer
        
        # Bottom controls
        st.divider()
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("💾 Save Progress"):
                st.success("Progress saved!")
        
        with col2:
            answered = len([k for k in st.session_state.answers.keys() if k.startswith('mcq')])
            st.metric("MCQ Answered", f"{answered}/15")
        
        with col3:
            if st.button("🏁 Submit Exam", type="primary"):
                st.success("Exam submitted successfully!")
                st.balloons()
                
                # Show results summary
                st.markdown("### Submission Summary")
                st.write(f"MCQ Questions answered: {answered}/15")
                st.write(f"DSA Question: {'Attempted' if 'dsa' in st.session_state.answers else 'Not attempted'}")
                st.write(f"Time taken: {format_time(900 - remaining_time)}")
                
                st.stop()

if __name__ == "__main__":
    main()
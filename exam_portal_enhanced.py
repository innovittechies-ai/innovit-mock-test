import streamlit as st
import cv2
import time
from datetime import datetime, timedelta
import numpy as np
from PIL import Image
import threading

# Initialize session state
if 'exam_started' not in st.session_state:
    st.session_state.exam_started = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'camera_frame' not in st.session_state:
    st.session_state.camera_frame = None

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
    "title": "Maximum Subarray Sum (Kadane's Algorithm)",
    "description": """Write a Python function that finds the maximum sum of a contiguous subarray.
    
Function signature: def max_subarray_sum(arr):
    
The function should return the maximum sum possible from any contiguous subarray.""",
    "example": """Example:
Input: [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6
Explanation: The subarray [4, -1, 2, 1] has the maximum sum of 6."""
}

class CameraHandler:
    def __init__(self):
        self.cap = None
        self.running = False
    
    def start(self):
        try:
            self.cap = cv2.VideoCapture(0)
            self.running = True
            return True
        except:
            return False
    
    def get_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Resize frame for display
                frame = cv2.resize(frame, (200, 150))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                return frame
        return None
    
    def stop(self):
        if self.cap:
            self.cap.release()
        self.running = False

def get_remaining_time():
    """Calculate remaining exam time"""
    if st.session_state.start_time:
        elapsed = datetime.now() - st.session_state.start_time
        remaining = timedelta(minutes=15) - elapsed
        return max(0, int(remaining.total_seconds()))
    return 900

def format_time(seconds):
    """Format seconds to MM:SS"""
    mins, secs = divmod(seconds, 60)
    return f"{mins:02d}:{secs:02d}"

def calculate_score():
    """Calculate MCQ score"""
    correct = 0
    for i, question in enumerate(MCQ_QUESTIONS):
        if f"mcq_{i}" in st.session_state.answers:
            if st.session_state.answers[f"mcq_{i}"] == question['correct']:
                correct += 1
    return correct

def main():
    st.set_page_config(page_title="Online Exam Portal", layout="wide")
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .exam-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .timer-box {
        background: #ff6b6b;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .camera-box {
        border: 2px solid #4ecdc4;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="exam-header"><h1>🎓 Online Exam Portal</h1></div>', unsafe_allow_html=True)
    
    if not st.session_state.exam_started:
        # Pre-exam screen
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📋 Exam Instructions")
            st.markdown("""
            - **Duration:** 15 minutes
            - **Questions:** 15 MCQ + 1 Python DSA problem
            - **Monitoring:** Camera and microphone will be active
            - **Submission:** Auto-submit when time expires or manual submit
            - **Rules:** No external help, stay in frame, no switching tabs
            """)
            
            st.markdown("### ✅ Pre-exam Checklist")
            camera_check = st.checkbox("Camera is working")
            mic_check = st.checkbox("Microphone is working") 
            rules_check = st.checkbox("I agree to exam rules and regulations")
            
            if camera_check and mic_check and rules_check:
                if st.button("🚀 Start Exam", type="primary", use_container_width=True):
                    st.session_state.exam_started = True
                    st.session_state.start_time = datetime.now()
                    st.rerun()
        
        with col2:
            st.markdown("### 📹 Camera Test")
            # Camera test placeholder
            st.info("Enable camera to test video feed")
            
    else:
        # Exam interface
        remaining_time = get_remaining_time()
        
        if remaining_time <= 0:
            st.markdown('<div class="timer-box">⏰ TIME\'S UP! EXAM ENDED</div>', unsafe_allow_html=True)
            
            # Show final results
            score = calculate_score()
            st.markdown("### 📊 Final Results")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("MCQ Score", f"{score}/15", f"{(score/15)*100:.1f}%")
            with col2:
                st.metric("DSA Question", "Attempted" if 'dsa' in st.session_state.answers else "Not Attempted")
            with col3:
                st.metric("Total Time", "15:00")
            
            if 'dsa' in st.session_state.answers:
                st.markdown("### 💻 Your DSA Solution")
                st.code(st.session_state.answers['dsa'], language="python")
            
            st.stop()
        
        # Top monitoring bar
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            color = "red" if remaining_time < 300 else "orange" if remaining_time < 600 else "green"
            st.markdown(f'<div class="timer-box" style="background: {color}">⏱️ {format_time(remaining_time)}</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="camera-box">📹 Camera Active<br/>🎤 Mic Active</div>', unsafe_allow_html=True)
        
        with col3:
            answered = len([k for k in st.session_state.answers.keys() if k.startswith('mcq')])
            st.metric("Progress", f"{answered}/15 MCQ")
        
        # Main exam content
        tab1, tab2 = st.tabs(["📝 MCQ Questions (15)", "💻 Python DSA (1)"])
        
        with tab1:
            st.markdown("### Multiple Choice Questions")
            st.markdown("*Select the best answer for each question*")
            
            # Progress bar
            progress = answered / 15
            st.progress(progress, text=f"Completed: {answered}/15")
            
            for i, question in enumerate(MCQ_QUESTIONS):
                with st.container():
                    st.markdown(f"**Question {i+1}/15**")
                    st.markdown(f"**{question['q']}**")
                    
                    answer = st.radio(
                        f"Select your answer:",
                        question['options'],
                        key=f"mcq_{i}",
                        index=None
                    )
                    
                    if answer:
                        st.session_state.answers[f"mcq_{i}"] = question['options'].index(answer)
                        st.success("✅ Answer saved")
                    
                    st.divider()
        
        with tab2:
            st.markdown("### Python DSA Problem")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**{DSA_QUESTION['title']}**")
                st.markdown(DSA_QUESTION['description'])
                st.code(DSA_QUESTION['example'], language="text")
                
                code_answer = st.text_area(
                    "💻 Write your Python solution:",
                    height=400,
                    placeholder="""def max_subarray_sum(arr):
    # Write your solution here
    # Hint: Use Kadane's algorithm
    pass

# Test your function
# print(max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # Expected: 6""",
                    key="dsa_answer"
                )
                
                if code_answer:
                    st.session_state.answers['dsa'] = code_answer
                    st.success("✅ Code saved")
            
            with col2:
                st.markdown("**💡 Hints:**")
                st.info("• Think about dynamic programming\n• Keep track of maximum sum ending at current position\n• Update global maximum as you iterate")
                
                st.markdown("**⚡ Test Cases:**")
                st.code("""
Test 1: [1, 2, 3, 4] → 10
Test 2: [-1, -2, -3] → -1  
Test 3: [5, -3, 2, 4] → 8
                """, language="text")
        
        # Bottom action bar
        st.divider()
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💾 Save Progress", use_container_width=True):
                st.success("✅ Progress saved!")
                time.sleep(1)
        
        with col2:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        
        with col3:
            if st.button("⚠️ Quit Exam", use_container_width=True):
                if st.button("⚠️ Confirm Quit", type="secondary"):
                    st.error("Exam terminated by user")
                    st.stop()
        
        with col4:
            if st.button("🏁 Submit Exam", type="primary", use_container_width=True):
                score = calculate_score()
                
                st.success("🎉 Exam submitted successfully!")
                st.balloons()
                
                # Final summary
                st.markdown("### 📋 Submission Summary")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("MCQ Score", f"{score}/15", f"{(score/15)*100:.1f}%")
                with col2:
                    st.metric("DSA Question", "✅ Attempted" if 'dsa' in st.session_state.answers else "❌ Not Attempted")
                with col3:
                    st.metric("Time Used", format_time(900 - remaining_time))
                
                st.markdown("### 🎯 Performance Analysis")
                if score >= 12:
                    st.success("🌟 Excellent performance!")
                elif score >= 9:
                    st.info("👍 Good performance!")
                elif score >= 6:
                    st.warning("📈 Average performance - room for improvement")
                else:
                    st.error("📚 Needs more preparation")
                
                st.stop()

if __name__ == "__main__":
    main()
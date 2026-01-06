import streamlit as st
import cv2
import time

from datetime import datetime, timedelta
import numpy as np

# Initialize session state
if 'exam_started' not in st.session_state:
    st.session_state.exam_started = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'camera_active' not in st.session_state:
    st.session_state.camera_active = False

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
    """Initialize camera"""
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            st.session_state.camera_active = True
            return cap
    except:
        st.error("Camera not accessible")
    return None

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
        
        if st.button("🚀 Start Exam", type="primary"):
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
        
        with col2:
            # Camera placeholder (simplified for demo)
            st.markdown("📹 **Camera Active**")
            st.markdown("🎤 **Mic Active**")
            # In real implementation, you'd show actual camera feed here
            st.image("https://via.placeholder.com/150x100/FF0000/FFFFFF?text=CAMERA", width=150)
        
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
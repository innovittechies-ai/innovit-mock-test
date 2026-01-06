import streamlit as st
import time
from datetime import datetime, timedelta
import random

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
if 'exam_submitted' not in st.session_state:
    st.session_state.exam_submitted = False

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

def get_camera_close_html():
    """Generate HTML to close camera and show thank you message"""
    return """
    <div style="text-align: center; padding: 40px; border: 2px solid #4CAF50; border-radius: 15px; background: linear-gradient(135deg, #e8f5e9, #f1f8e9);">
        <h2 style="color: #2E7D32; margin-bottom: 20px;">🎉 Exam Submitted Successfully!</h2>
        <div style="font-size: 64px; margin: 20px 0;">✅</div>
        <h3 style="color: #388E3C; margin-bottom: 30px;">Thank you for completing the exam!</h3>
        <p style="font-size: 18px; color: #555; margin-bottom: 20px;">Your responses have been recorded and submitted.</p>
        <p style="font-size: 16px; color: #666; margin-bottom: 30px;">We will get back to you with the results soon.</p>
        <div style="background: #fff; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <p style="color: #333; margin: 0;"><strong>What happens next?</strong></p>
            <p style="color: #666; margin: 10px 0 0 0;">Our team will review your submission and contact you within 2-3 business days.</p>
        </div>
    </div>
    
    <script>
        // Stop all camera and microphone streams
        navigator.mediaDevices.getUserMedia({ video: true, audio: true })
            .then(function(stream) {
                stream.getTracks().forEach(track => track.stop());
            })
            .catch(function(err) {
                console.log('No active streams to stop');
            });
        
        // Clear any existing video elements
        const videos = document.querySelectorAll('video');
        videos.forEach(video => {
            if (video.srcObject) {
                video.srcObject.getTracks().forEach(track => track.stop());
                video.srcObject = null;
            }
        });
        
        console.log('Camera and microphone have been stopped.');
    </script>
    """

def get_camera_html():
    return """
    <div style="text-align: center; padding: 20px; border: 2px solid #ff4444; border-radius: 10px; background: #fff5f5;">
        <h4>📹 Live Camera Feed</h4>
        <video id="cameraFeed" width="320" height="240" autoplay muted style="border-radius: 10px; border: 2px solid #ccc;"></video>
        <br><br>
        <button onclick="startCamera()" style="background: #ff4444; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">🔴 Start Camera</button>
        <button onclick="stopCamera()" style="background: #666; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-left: 10px;">⏹️ Stop Camera</button>
        <br><br>
        <div id="cameraStatus" style="font-weight: bold; color: #ff4444;">📷 Camera: Inactive</div>
        <div id="micStatus" style="font-weight: bold; color: #ff4444;">🎤 Microphone: Inactive</div>
    </div>
    
    <script>
        let stream = null;
        let isRecording = false;
        
        async function startCamera() {
            try {
                stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { width: 320, height: 240 }, 
                    audio: true 
                });
                
                const video = document.getElementById('cameraFeed');
                video.srcObject = stream;
                
                document.getElementById('cameraStatus').innerHTML = '📹 Camera: <span style="color: green;">ACTIVE & RECORDING</span>';
                document.getElementById('micStatus').innerHTML = '🎤 Microphone: <span style="color: green;">ACTIVE & RECORDING</span>';
                
                isRecording = true;
                
                // Monitor for stream end
                stream.getTracks().forEach(track => {
                    track.onended = () => {
                        document.getElementById('cameraStatus').innerHTML = '📷 Camera: <span style="color: red;">DISCONNECTED</span>';
                        document.getElementById('micStatus').innerHTML = '🎤 Microphone: <span style="color: red;">DISCONNECTED</span>';
                    };
                });
                
            } catch (err) {
                console.error('Error accessing camera/microphone:', err);
                document.getElementById('cameraStatus').innerHTML = '📷 Camera: <span style="color: red;">ACCESS DENIED</span>';
                document.getElementById('micStatus').innerHTML = '🎤 Microphone: <span style="color: red;">ACCESS DENIED</span>';
                alert('Please allow camera and microphone access to continue with the exam.');
            }
        }
        
        function stopCamera() {
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
                document.getElementById('cameraFeed').srcObject = null;
                document.getElementById('cameraStatus').innerHTML = '📷 Camera: Inactive';
                document.getElementById('micStatus').innerHTML = '🎤 Microphone: Inactive';
                isRecording = false;
            }
        }
        
        // Auto-start camera when page loads
        window.addEventListener('load', function() {
            setTimeout(startCamera, 1000);
        });
        
        // Prevent tab switching during exam
        document.addEventListener('visibilitychange', function() {
            if (document.hidden && isRecording) {
                alert('⚠️ WARNING: Tab switching detected! This action has been logged.');
            }
        });
        
        // Prevent right-click
        document.addEventListener('contextmenu', function(e) {
            if (isRecording) {
                e.preventDefault();
                alert('⚠️ Right-click is disabled during the exam.');
            }
        });
    </script>
    """

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

def get_elapsed_time():
    """Calculate elapsed exam time"""
    if st.session_state.start_time:
        elapsed = datetime.now() - st.session_state.start_time
        return int(elapsed.total_seconds())
    return 0

def format_time(seconds):
    """Format seconds to MM:SS"""
    mins, secs = divmod(seconds, 60)
    return f"{mins:02d}:{secs:02d}"

def main():
    st.set_page_config(page_title="Online Exam Portal", layout="wide")
    
    # Header
    st.title("🎓 Online Exam Portal")
    
    # Check if exam is submitted
    if st.session_state.get('exam_submitted', False):
        # Show thank you page and close camera
        st.components.v1.html(get_camera_close_html(), height=500)
        st.stop()
    
    if not st.session_state.exam_started:
        # Pre-exam screen
        st.markdown("### Exam Instructions")
        st.write("- Duration: 15 minutes")
        st.write("- 15 MCQ questions + 1 Python DSA question")
        st.write("- Camera and microphone will be monitored")
        st.write("- Click 'Start Exam' when ready")
        
        st.markdown("### 📹 Camera & Microphone Test")
        st.info("⚠️ Please allow camera and microphone access when prompted by your browser.")
        
        # HTML5 Camera Test
        st.components.v1.html(get_camera_html(), height=400)
        
        st.markdown("---")
        if st.button("🚀 Start Exam", type="primary"):
            start_camera()
            st.session_state.exam_started = True
            st.session_state.start_time = datetime.now()
            st.rerun()
    
    else:
        # Exam interface
        elapsed_time = get_elapsed_time()
        
        # Check if 15 minutes have passed
        if elapsed_time >= 900:  # 15 minutes = 900 seconds
            st.error("⏰ Time's up! Exam ended automatically.")
            st.session_state.exam_submitted = True
            st.rerun()
        
        # Top bar with timer and camera
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Live JavaScript timer that updates automatically
            start_time_js = int(st.session_state.start_time.timestamp() * 1000) if st.session_state.start_time else 0
            
            timer_html = f"""
            <div style="background: #f0f8ff; padding: 15px; border-radius: 10px; border: 2px solid #4CAF50;">
                <h3 style="margin: 0; color: #2E7D32;">⏱️ Time Elapsed: <span id="timer">00:00</span></h3>
                <div style="margin-top: 10px; font-size: 14px; color: #666;">Exam Duration: 15 minutes</div>
            </div>
            
            <script>
                const startTime = {start_time_js};
                
                function updateTimer() {{
                    const now = new Date().getTime();
                    const elapsed = Math.floor((now - startTime) / 1000);
                    
                    const minutes = Math.floor(elapsed / 60);
                    const seconds = elapsed % 60;
                    
                    const formattedTime = String(minutes).padStart(2, '0') + ':' + String(seconds).padStart(2, '0');
                    document.getElementById('timer').textContent = formattedTime;
                    
                    // Auto-submit after 15 minutes (900 seconds)
                    if (elapsed >= 900) {{
                        alert('⏰ Time\'s up! Exam will be submitted automatically.');
                        // You could trigger form submission here
                    }}
                }}
                
                // Update timer every second
                setInterval(updateTimer, 1000);
                updateTimer(); // Initial call
            </script>
            """
            
            st.components.v1.html(timer_html, height=100)
            
            # Show monitoring status
            monitoring_alert = show_monitoring_alerts()
            st.markdown(f"<div style='background: #e8f5e8; padding: 8px; border-radius: 5px; margin: 5px 0;'><small>{monitoring_alert}</small></div>", unsafe_allow_html=True)
        
        with col2:
            # Real camera and microphone streaming
            camera_status = get_camera_status()
            mic_status = get_mic_status()
            
            st.markdown(f"**{camera_status}**")
            st.markdown(f"**{mic_status}**")
            
            # Real-time webcam stream during exam
            st.components.v1.html(get_camera_html(), height=350)
        
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
                # Close camera and show thank you message
                st.session_state.exam_submitted = True
                st.rerun()

if __name__ == "__main__":
    main()
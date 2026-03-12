from flask import Flask, render_template, request, jsonify
import sys
import os
import threading

# Add the parent directory to the path 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import config
    from robot_control.arm_controller import trigger_gesture
except ImportError:
    config = None
    config = None
    trigger_gesture = lambda x: print(f"Mock Dashboard Trigger: {x}")

# Initialize camera feed
try:
    import cv2
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Warning: Could not open camera for dashboard.")
        camera = None
except ImportError:
    print("Warning: cv2 not found, camera feed will be unavailable.")
    camera = None
    
app = Flask(__name__)

# Basic state store for dashboard UI
dashboard_state = {
    "status": "Online",
    "last_command": "None",
    "last_gesture_detected": "None",
    "inventory_api_status": "Checking..."
}

# 10 minute continuous mimic state
continuous_mimic_until = 0

def update_state(key: str, value: str):
    """Callback to let main loop update dashboard parameters."""
    dashboard_state[key] = value

@app.route("/")
def landing():
    return render_template('landing.html')

@app.route("/dashboard")
def index():
    return render_template('index.html', state=dashboard_state)

def generate_frames():
    """Generator function to yield camera frames as a continuous stream with gesture detection."""
    global continuous_mimic_until
    import time
    last_gesture_time = 0
    
    try:
        import mediapipe as mp
        from gesture.wave_detector import detect_gesture_type
        mp_hands = mp.solutions.hands
        mp_drawing = mp.solutions.drawing_utils
        hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
    except Exception as e:
        print(f"Failed to initialize MediaPipe in dashboard: {e}")
        hands = None

    while camera and camera.isOpened():
        success, frame = camera.read()
        if not success:
            break
        else:
            if hands is not None:
                # Process with MediaPipe
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image)
                image.flags.writeable = True

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        
                        g_type = detect_gesture_type(hand_landmarks)
                        if g_type not in ["unknown", "none"]:
                            update_state("last_gesture_detected", g_type.capitalize())
                            
                            is_continuous_mimic = (time.time() < continuous_mimic_until)
                            debounce_time = 1.0 if is_continuous_mimic else 4.0
                            
                            # Mimic the gesture (faster debounce if strictly mimicking)
                            if time.time() - last_gesture_time > debounce_time:
                                trigger_gesture(g_type.upper())
                                mode_text = "Continuous Mimic" if is_continuous_mimic else "Auto-Mimic"
                                update_state("last_command", f"{mode_text}: {g_type}")
                                last_gesture_time = time.time()

            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            # Yield multipart stream using MJPEG format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    from flask import Response
    if camera:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Camera feed not available", 404

@app.route("/api/trigger_gesture", methods=['POST'])
def api_trigger_gesture():
    """REST Endpoint to trigger robot gestures remotely."""
    data = request.json
    gesture = data.get('gesture')
    if gesture:
        trigger_gesture(gesture)
        update_state("last_command", f"Dashboard Override: {gesture}")
        return jsonify({"status": "success", "message": f"Triggered {gesture}"})
    return jsonify({"status": "error", "message": "No gesture provided"}), 400

@app.route("/api/start_mimic", methods=['POST'])
def api_start_mimic():
    """REST Endpoint to start 10 minutes of continuous hand tracking mimicry."""
    import time
    global continuous_mimic_until
    continuous_mimic_until = time.time() + 600 # 10 minutes
    update_state("last_command", "Started 10 Min Mimic Mode")
    return jsonify({"status": "success", "message": "Continuous mimic mode started for 10 minutes."})
    
def start_dashboard():
    """Starts the Flask server in a separate thread."""
    host = getattr(config, 'DASHBOARD_HOST', "0.0.0.0") if config else "0.0.0.0"
    port = getattr(config, 'DASHBOARD_PORT', 5000) if config else 5000
    
    flask_thread = threading.Thread(
        target=app.run, 
        kwargs={'host': host, 'port': port, 'debug': False, 'use_reloader': False},
        daemon=True
    )
    flask_thread.start()
    print(f"Flask Dashboard running on http://{host}:{port}")
    return update_state

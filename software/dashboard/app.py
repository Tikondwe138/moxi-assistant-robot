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

def update_state(key: str, value: str):
    """Callback to let main loop update dashboard parameters."""
    dashboard_state[key] = value

@app.route("/")
def index():
    return render_template('index.html', state=dashboard_state)

def generate_frames():
    """Generator function to yield camera frames as a continuous stream."""
    while camera and camera.isOpened():
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Yield multipart stream using MJPEG format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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

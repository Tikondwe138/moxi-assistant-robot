import cv2
<<<<<<< HEAD
import mediapipe as mp
import time
import sys
import os

# Add the parent directory to the path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import config
except ImportError:
    config = None

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def detect_gesture_type(hand_landmarks) -> str:
    """
    Classify the hand landmark configuration.
    
    Args:
        hand_landmarks: The normalized landmark list from MediaPipe.
        
    Returns:
        str: "wave", "thumbs-up", "point", or "unknown"
    """
    # Grab Y coordinates of fingertips and corresponding PIP joints
    # MediaPipe Landmarks: 8 (Index tip), 6 (Index PIP), 12 (Middle tip), 10 (Middle PIP)
    # 16 (Ring tip), 14 (Ring PIP), 20 (Pinky tip), 18 (Pinky PIP), 4 (Thumb tip), 3 (Thumb IP)
    
    fingers_open = [
        hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y,   # Index
        hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y, # Middle
        hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y, # Ring
        hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y  # Pinky
    ]
    
    thumb_is_open = hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x # Basic heuristic for right hand thumb
    
    # All fingers open except thumb = Wave
    if sum(fingers_open) >= 4:
        return "wave"
        
    # Only thumb open, others closed = Thumbs-up
    if sum(fingers_open) == 0 and thumb_is_open:
        # Check if thumb is pointing up
        if hand_landmarks.landmark[4].y < hand_landmarks.landmark[3].y:
            return "thumbsup"
            
    # Index open, others closed = Point
    if fingers_open[0] and sum(fingers_open[1:]) == 0:
        return "point"
        
    return "unknown"

def detect_wave(duration: int = 3) -> bool:
    """Backward compatible wrapper. Returns True if any gesture is detected."""
    res = detect_gesture(duration)
    return res != "none"

def detect_gesture(duration: int = 3) -> str:
    """
    Detect multiple hand gestures using MediaPipe.
    
    Args:
        duration (int): How long to watch for a gesture in seconds.
        
    Returns:
        str: The name of the detected gesture, or "none".
    """
    if config and hasattr(config, 'GESTURE_TIMEOUT'):
        duration = config.GESTURE_TIMEOUT
        
    sensitivity = config.GESTURE_SENSITIVITY if config and hasattr(config, 'GESTURE_SENSITIVITY') else 0.8
    
=======
import time

def detect_wave(duration: int = 5) -> bool:
    """
    Detect human waving using camera input by analyzing motion within the frame.
    
    Args:
        duration (int): How long to watch for a wave in seconds.
        
    Returns:
        bool: True if a wave gesture is detected, False otherwise.
    """
>>>>>>> a7f7ddf (VERSION 02)
    # Open the default camera feed
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera for gesture detection.")
<<<<<<< HEAD
        return "none"
        
    detected_gesture = "none"
    start_time = time.time()
    
    print("Initializing MediaPipe Vision Tracking...")
    
    try:
        with mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=sensitivity,
            min_tracking_confidence=sensitivity) as hands:
                
            while time.time() - start_time < duration:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                # To improve performance, optionally mark the image as not writeable
                frame.flags.writeable = False
                # Convert BGR to RGB for MediaPipe
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(image)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Classify the gesture
                        g_type = detect_gesture_type(hand_landmarks)
                        if g_type != "unknown":
                            detected_gesture = g_type
                            print(f"Vision AI detected gesture: {g_type}")
                            return detected_gesture # Immediate return on detection
                            
                # Optional: Add small delay to free CPU
                time.sleep(0.05)
                
    finally:
        cap.release()
        
    return detected_gesture
=======
        return False
        
    # Read the first frame and convert to grayscale
    ret, frame1 = cap.read()
    if not ret:
        cap.release()
        return False
        
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)
    
    motion_detected = False
    start_time = time.time()
    motion_count = 0
    
    print("Watching for a wave...")
    try:
        while time.time() - start_time < duration:
            # Read the next frame
            ret, frame2 = cap.read()
            if not ret:
                break
                
            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)
            
            # Compute the absolute difference between the current and previous frame
            diff = cv2.absdiff(gray1, gray2)
            
            # Threshold the difference image
            thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            
            # Find contours maps to the regions of motion
            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Ignore small movements
                if cv2.contourArea(contour) < 5000:
                    continue
                motion_count += 1
                
            # If we sequence enough fast changing frames, consider it a wave
            if motion_count > 10:
                motion_detected = True
                print("Wave gesture detected!")
                break
                
            # Advance frame
            gray1 = gray2
            
            # Optional: Allow slight delay to reduce CPU blast
            time.sleep(0.05)
            
    finally:
        # Make sure we always release the camera
        cap.release()
        
    return motion_detected
>>>>>>> a7f7ddf (VERSION 02)

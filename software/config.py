# Serial port configuration
SERIAL_PORT = "/dev/ttyUSB0"
SERIAL_BAUD = 9600

# Inventory API endpoint
INVENTORY_API = "https://studio-website/api/inventory"

# Microphone configuration
MIC_INDEX = 1  
MIC_SAMPLE_RATE = 44100

# Voice settings
VOICE_RATE = 160
VOICE_VOLUME = 1.0

# Speech Session Config
SPEECH_TIMEOUT = 5
PHRASE_TIME_LIMIT = 15

# Gesture Detection Config
GESTURE_SENSITIVITY = 0.8  # Threshold for MediaPipe hand detection confidence
GESTURE_TIMEOUT = 3.0      # Seconds to watch for a gesture

# Multi-Joint Arm Configuration (Shoulder, Elbow, Wrist limits)
JOINT_LIMITS = {
    "shoulder": (0, 180),
    "elbow": (0, 180),
    "wrist": (0, 180)
}

# Dashboard Configuration
DASHBOARD_HOST = "0.0.0.0"
DASHBOARD_PORT = 5000

# MOXI v2 Enhancements

## 1. Vision Tracking (MediaPipe)
Replaced simple motion detection with `mediapipe` hand-landmark detection. MOXI now natively understands:
- Wave (Open hand, fingers separated)
- Thumbs-up (Closed fist, thumb extended upward)
- Pointing (Index finger extended)

## 2. Advanced Speech Processing and NLP
`speech_recognition` upgraded with background noise calibration and dynamic energy thresholds. It captures phrases continually until a timeout, pushing a queue of sentences into the system.
The system uses `spaCy` to extract user intents (Greetings, Inventory, Contacts, Exits) and Entity mapping (e.g., pulling "PLA filament" out of "Is the PLA filament in stock").

## 3. Asynchronous 3-DoF Robotic Arm
The physical arm structure upgraded from 1 servo to 3 (Shoulder, Elbow, Wrist). The Arduino handles smoothing calculations `smoothMove()` to prevent jerky movements.
The Python driver `arm_controller.py` utilizes a background Thread and a Queue (`deque`) to allow MOXI to queue up sequences of physical gestures without halting the main audio listening loop.

## 4. Web Dashboard
Included a lightweight `Flask` dashboard running silently on `http://0.0.0.0:5000`. 
Features:
- Live display of MOXI State, last voice command heard, and API health.
- REST endpoints allowing users to manually trigger a wave, thumbs-up, or point.

## 5. Centralized Logging
Implemented standard Python logging mapping simultaneously to the `sys.stdout` stream and a file at `logs/moxi.log`. 
Additionally, all inventory requests are transparently saved in CSV format to `logs/inventory_queries.csv` for data science extraction.

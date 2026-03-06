# MOXI System Architecture (v2.0)

## System Layers
1. **Cognitive processing layer (speech/vision):** 
   Python scripts on the host utilizing `speechrecognition` for text capture and `mediapipe` for AI hand-landmark geometry tracking.
2. **Natural Language Processing (NLP) layer:**
   Powered by `spaCy`, extracts structural intent and entities from raw microphone text.
3. **Orchestration layer (main loop) & UI Dashboard:**
   `main.py` controller processes intends sequentially. `Flask` UI runs asynchronously in a Thread supplying a visual window into the brain parameters.
4. **Services API layer:**
   Integrates `inventory_api.py` with multi-query capacity and retry safety, backed by robust file logging.
5. **Hardware abstraction side (serial):**
   A threaded Task Queue pushing string commands sequentially over USB via `pyserial`.
6. **Physical execution layer:**
   The Arduino Uno running `moxi_servo_controller.ino`. Controls 3-DoF via interpolation smoothing functions.

## Communication Flow
`Speech -> Python Mic -> Text -> spacy NLP -> String Intent -> Main Controller`
`Gesture UI -> Flask REST API -> Thread-Safe Queue -> PySerial -> Arduino 3-DoF -> Smooth Servo Sweep`

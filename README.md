# MOXI (Multi-Operational eXperimental Interface)

## Acronym Explanation
**MOXI** stands for Multi-Operational eXperimental Interface.

## Project Description
MOXI is a modern, robotic design studio assistant designed to be the interactive heart of the studio workspace. Capable of seamlessly interacting with visitors and accessing studio resources, MOXI represents the intersection of hardware engineering, software automation, and interactive design. It assists in daily studio operations, greets visitors, processes speech and gestures, and integrates with the digital systems of the studio environment.

## System Architecture
The MOXI system is built on a distributed architecture comprising:
1. **Core Software Controller (Python):** Handles high-level logic, including speech recognition, intent processing, API communication, and gesture detection.
2. **Web Dashboard (Flask):** Provides a visual interface with live camera feed and manual control overrides.
3. **Hardware Controller (Arduino):** Manages low-level hardware components, specifically servo control for physical movement.
4. **Communication Layer:** A serial interface (`pyserial`) linking the core software controller with the Arduino microprocessor.
5. **Services Layer:** Integrates with external or internal APIs (e.g., Inventory APIs, Contact Services) to provide useful contextual information.

## Hardware Requirements
- **Compute:** A dedicated computer or microcomputer (e.g., Raspberry Pi or standard PC) running the Python core.
- **Microcontroller:** Arduino Uno/Mega or compatible board for motor control.
- **Actuators:** Servo motors for robotic arm movement and expressions.
- **Sensors/Input:**
  - Microphones for audio input.
  - Webcam or camera module for gesture detection.
- **Output:**
  - Speakers for synthesized speech output.
- **Wiring:** Standard jumper wires, breadboards, and power supplies suitable for the connected servo motors.

- **Software Stack**
  - Language: Python 3.9+
  - Microcontroller Firmware: C++ (Arduino IDE)
  - Key Python Libraries:
    - `speechrecognition` (Audio input and STT)
    - `pyttsx3` (Text-to-Speech output, configured with a female voice)
    - `Flask` (Web dashboard with live camera feed)
    - `requests` (API integrations)
    - `pyserial` (Serial communication with Arduino)
    - `pyaudio` (Audio stream processing)
    - `opencv-python` (Computer vision and gesture detection)
    - `mediapipe` (Advanced hand tracking)

## Installation Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-org/moxi-assistant-robot.git
   cd moxi-assistant-robot
   ```

2. **Set up the Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Copy the example environment file and configure your API keys and serial port setting.
   ```bash
   cp .env.example .env
   ```

5. **Hardware Setup:**
   - Upload `hardware/arduino_controller/moxi_servo_controller.ino` to your Arduino using the Arduino IDE.
   - Refer to `docs/hardware_setup.md` or `hardware/wiring_diagram.png` for instructions on wiring the physical robot.

6. **Web Dashboard:**
   - The Flask dashboard will automatically start on `http://localhost:5000`. You can monitor the system status, view the live camera feed, and manually trigger gestures from there.

## Usage Examples

**1. Starting the core assistant:**
```bash
python software/main.py
```

**2. Example Interaction (Speech):**
- **Visitor:** "Hello MOXI, who is in the studio today?"
- **MOXI (via Speech Output):** "Let me check the contacts service. Alice and Bob are currently present."

**3. Available Voice Commands:**
Chat with MOXI using the following commands:
- "Hello" or "Hi Moxi" (Greets the assistant and triggers a wave)
- "Find contact [Name]" (Looks up a phone number)
- "Check inventory for [Item]" (Checks stock availability)
- "Execute [gesture] gesture" (Triggers a robot action, e.g. "Execute point gesture")
- "Exit" or "Shut down" (Safely shuts down the MOXI system)

**4. Example Interaction (Gesture):**
- *Visitor waves at the camera.*
- *MOXI detects the wave using `opencv-python`, triggering the Arduino to move the robotic arm and wave back.*

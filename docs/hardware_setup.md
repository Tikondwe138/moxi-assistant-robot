# Hardware Setup

## Arduino Connection
1. Connect via standard USB A-to-B. Set `SERIAL_PORT` in `software/config.py`.

## 3-DoF Servo Motor Wiring
1. Provide a **separate robust 5V power supply (At least 3 Amps)** to the Servo array.
2. Unify the Ground of the External Power with the Ground of the Arduino.
3. Connect all Servo Red wires to External 5V payload.
4. Connect Signal pins:
   - **Shoulder Servo:** Arduino Digital Pin 9
   - **Elbow Servo:** Arduino Digital Pin 10
   - **Wrist Servo:** Arduino Digital Pin 11

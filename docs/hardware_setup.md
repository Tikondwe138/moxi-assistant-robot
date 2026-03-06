# Hardware Setup

## Arduino Connection
<<<<<<< HEAD
1. Connect via standard USB A-to-B. Set `SERIAL_PORT` in `software/config.py`.

## 3-DoF Servo Motor Wiring
1. Provide a **separate robust 5V power supply (At least 3 Amps)** to the Servo array.
2. Unify the Ground of the External Power with the Ground of the Arduino.
3. Connect all Servo Red wires to External 5V payload.
4. Connect Signal pins:
   - **Shoulder Servo:** Arduino Digital Pin 9
   - **Elbow Servo:** Arduino Digital Pin 10
   - **Wrist Servo:** Arduino Digital Pin 11
=======
1. Connect the Arduino via a standard USB A-to-B cable to the host machine.
2. The Arduino must be identified to the OS. Note the port (e.g., `/dev/ttyUSB0` or `COM3`) and configure it under `software/config.py` in `SERIAL_PORT`.

## Servo Motor Wiring
1. Provide a **separate 5V power supply** to the Servo Motor(s). The Arduino 5V pin WILL NOT provide enough current to sustain sudden robotic arm movements.
2. `Ground (Brown/Black wire)` on the servo connects to the ground of the external 5V power supply, AND the ground of the Arduino to unify the logical connection.
3. `Power (Red wire)` on the servo connects strictly to the 5V out of the external 5V power module.
4. `Signal (Yellow/Orange wire)` on the servo connects to Digital Pin 9 on the Arduino Uno.

If the Arduino resets when the servo begins moving, it indicates an insufficient external power source and power is drawing down too heavily, browning out the microcontroller.
>>>>>>> a7f7ddf (VERSION 02)

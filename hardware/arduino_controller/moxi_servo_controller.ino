#include <Servo.h>

// 3-Degree of Freedom Robotics Arm setup
Servo shoulderServo;
Servo elbowServo;
Servo wristServo;

const int shoulderPin = 9;
const int elbowPin = 10;
const int wristPin = 11;

void setup() {
  shoulderServo.attach(shoulderPin);
  elbowServo.attach(elbowPin);
  wristServo.attach(wristPin);

  // Set initial neutral position
  moveToNeutral();

  // Initialize serial communication
  Serial.begin(9600);
  while (!Serial) {
    ;
  }
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    // Parse gesture type
    if (command == "WAVE") {
      executeWave();
      Serial.println("DONE");
    } else if (command == "THUMBSUP") {
      executeThumbsUp();
      Serial.println("DONE");
    } else if (command == "POINT") {
      executePoint();
      Serial.println("DONE");
    } else if (command == "GREET") {
      executeGreet();
      Serial.println("DONE");
    } else if (command == "STOP") {
      executeStop();
      Serial.println("DONE");
    } else if (command == "RESET") {
      executeReset();
      Serial.println("DONE");
    }
  }
}

// Custom easing function to smooth out jerky movements
void smoothMove(Servo &targetServo, int targetAngle, int speedDelay = 15) {
  int currentAngle = targetServo.read();

  if (currentAngle < targetAngle) {
    for (int pos = currentAngle; pos <= targetAngle; pos += 2) {
      targetServo.write(pos);
      delay(speedDelay);
    }
  } else {
    for (int pos = currentAngle; pos >= targetAngle; pos -= 2) {
      targetServo.write(pos);
      delay(speedDelay);
    }
  }
}

void moveToNeutral() {
  smoothMove(shoulderServo, 90, 10);
  smoothMove(elbowServo, 90, 10);
  smoothMove(wristServo, 90, 10);
}

void executeWave() {
  // Wave uses mostly shoulder and wrist
  smoothMove(shoulderServo, 70);
  smoothMove(elbowServo, 120);

  for (int i = 0; i < 3; i++) {
    smoothMove(wristServo, 45, 10);
    smoothMove(wristServo, 135, 10);
  }

  moveToNeutral();
}

void executeThumbsUp() {
  smoothMove(shoulderServo, 120);
  smoothMove(elbowServo, 45);
  smoothMove(wristServo, 180);
  delay(1000); // Hold gesture
  moveToNeutral();
}

void executePoint() {
  smoothMove(shoulderServo, 90);
  smoothMove(elbowServo, 180); // Fully extend elbow
  smoothMove(wristServo, 90);
  delay(1500); // Hold point
  moveToNeutral();
}

void executeGreet() {
  smoothMove(shoulderServo, 110);
  smoothMove(elbowServo, 110);
  smoothMove(wristServo, 45, 10);
  smoothMove(wristServo, 135, 10);
  moveToNeutral();
}

void executeStop() {
  shoulderServo.write(shoulderServo.read());
  elbowServo.write(elbowServo.read());
  wristServo.write(wristServo.read());
}

void executeReset() {
  moveToNeutral();
}

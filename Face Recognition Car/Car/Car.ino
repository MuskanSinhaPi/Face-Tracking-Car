#include <AFMotor.h>
#include <SoftwareSerial.h>

AF_DCMotor left(1);
AF_DCMotor right(3);

//SoftwareSerial XBee(4,5); // RX, TX pins
int direction;

void setup()
{
  Serial.begin(9600);
  // XBee.begin(9600);
  left.setSpeed(200);
  right.setSpeed(200);
  left.run(RELEASE);
  right.run(RELEASE);
}

void loop() {
//    if (XBee.available()) { //receive
  if (Serial.available()>0) { //receive
    direction = Serial.parseInt();
    Serial.println(direction);
    }

  switch (direction) {
    case 1:  // Back Left
      moveForward();
      break;
    case 2:  // Back
      moveBack();
      break;
    case 3:  // Back right
      moveLeft();
      break;
    case 4:  // Left
      moveRight();
      break;
    case 5:  // Stay still
      stopMoving();
      break;
//    case 6:  // Right
//      
//      break;
//    case 7:  // Front Left
//      moveForwardLeft();
//      break;
//    case 8:  // Forward
//      
//      break;
//    case 9:  // Forward right
//      moveForwardRight();
//      break;
    default: // Unknown direction or stay still
      stopMoving();
      break;
  }

}


void moveForward() {
  left.run(BACKWARD);
  right.run(BACKWARD);
  left.setSpeed(200);
  right.setSpeed(200);
}

void moveBack() {
  left.run(FORWARD);
  right.run(FORWARD);
  left.setSpeed(200);
  right.setSpeed(200);
}

void moveLeft() {
  left.run(RELEASE);
  right.run(BACKWARD);
  right.setSpeed(200);
}

void moveRight() {
  left.run(BACKWARD);
  right.run(RELEASE);
  left.setSpeed(200);
}

void moveForwardLeft() {
  left.run(BACKWARD);
  right.run(BACKWARD);
  left.setSpeed(200);
  right.setSpeed(400);
}

void moveForwardRight() {
  left.run(BACKWARD);
  right.run(BACKWARD);
  left.setSpeed(400);
  right.setSpeed(200);
}

void moveBackLeft() {
  left.run(FORWARD);
  right.run(FORWARD);
  left.setSpeed(200);
  right.setSpeed(400);
}

void moveBackRight() {
  left.run(FORWARD);
  right.run(FORWARD);
  left.setSpeed(400);
  right.setSpeed(200);
}

void stopMoving() {
  left.run(RELEASE);
  right.run(RELEASE);
}

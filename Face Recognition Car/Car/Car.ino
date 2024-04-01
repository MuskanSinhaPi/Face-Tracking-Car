#include <AFMotor.h>
#include <SoftwareSerial.h>
int data[1];

AF_DCMotor left(1);
AF_DCMotor right(3);
//const int leftMotorPin1 = 2;
//const int leftMotorPin2 = 3;
//const int rightMotorPin1 = 4;
//const int rightMotorPin2 = 5;

//SoftwareSerial XBee(4,5); // RX, TX pins

//int vspeed=100;    
//int tspeed=255;
//int tdelay=20;

void setup()
{
 Serial.begin(9600);
// XBee.begin(9600);
 left.setSpeed(200);
 right.setSpeed(200);
 left.run(RELEASE);
 right.run(RELEASE);
//
//  pinMode(leftMotorPin1, OUTPUT);
//  pinMode(leftMotorPin2, OUTPUT);
//  pinMode(rightMotorPin1, OUTPUT);
//  pinMode(rightMotorPin2, OUTPUT);
}

void loop() {
//  if (XBee.available()) { //receive
    if (Serial.available()) { //receive
      int direction = Serial.read();
      processDirection(direction);
  }
}

void processDirection(int direction) {
  switch (direction) {
    case 1:  // Back Left
      moveBackLeft();
      break;
    case 2:  // Back
      moveBack();
      break;
    case 3:  // Back right
      moveBackRight();
      break;
    case 4:  // Left
      moveLeft();
      break;
    case 5:  // Stay still
      stopMoving();
      break;
    case 6:  // Right
      moveRight();
      break;
    case 7:  // Front Left
      moveForwardLeft();
      break;
    case 8:  // Forward
      moveForward();
      break;
    case 9:  // Forward right
      moveForwardRight();
      break;
    default: // Unknown direction or stay still
      stopMoving();
      break;
  }
}

void moveForward() {
  left.run(FORWARD);
  right.run(FORWARD);
  left.setSpeed(200);
  right.setSpeed(200);
}

void moveBack() {
  left.run(BACKWARD);
  right.run(BACKWARD);
  left.setSpeed(200);
  right.setSpeed(200);
}

void moveLeft() {
  left.run(RELEASE);
  right.run(FORWARD);
  right.setSpeed(200);
}

void moveRight() {
  left.run(FORWARD);
  right.run(RELEASE);
  left.setSpeed(200);
}

void moveForwardLeft() {
  left.run(FORWARD);
  right.run(FORWARD);
  left.setSpeed(200);
  right.setSpeed(400);
}

void moveForwardRight() {
  left.run(FORWARD);
  right.run(FORWARD);
  left.setSpeed(400);
  right.setSpeed(200);
}

void moveBackLeft() {
  left.run(BACKWARD);
  right.run(BACKWARD);
  left.setSpeed(200);
  right.setSpeed(400);
}

void moveBackRight() {
  left.run(BACKWARD);
  right.run(BACKWARD);
  left.setSpeed(400);
  right.setSpeed(200);
}

void stopMoving() {
  left.run(RELEASE);
  right.run(RELEASE);
}
//   
//  if(c=='f')
//  {
//  forward(); 
//  }
//
//  else if(c=='l')
//  {
//  left(); 
//  }
// 
//  else if(c=='r')
//   { 
//  right(); 
//  }
//  
//  else if(c=='s')
//   {
//  none(); 
//  }
//}
//
//void forward() {
//digitalWrite(m1, HIGH);
//digitalWrite(m2, HIGH);
//}
////
////void back() {
////digitalWrite(leftMotorBackward,  HIGH);
////digitalWrite(rightMotorBackward, HIGH);
////digitalWrite(leftMotorForward,  LOW);
////digitalWrite(rightMotorForward, LOW);
////}
//
//void left() {
//digitalWrite(m1, LOW);
//digitalWrite(m2, HIGH);
//}
//
//void  right() {
//digitalWrite(m1, HIGH);
//digitalWrite(m2,  LOW);
//}
//
//void none() {
//digitalWrite(m1, LOW);
//digitalWrite(m2, LOW);
//}

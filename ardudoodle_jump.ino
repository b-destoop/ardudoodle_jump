#include <AbstractController.h>
#include <Hapkit.h>
#include <Motor.h>
#include <OpenLoopController.h>

/* void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.write(45); // send a byte with the value 45
  int bytesSent = Serial.write("meep");  //send the string "hello" and return the length of the string.
} */

unsigned long prev = 0; 
float force;
float relativePosition;
float incomingWind = 0;

void virtualCoupling(Hapkit &hapkit) {
  static const float damping = 0.05; //0.03;
  static const float stiffness = 1.0; //1.0;
  static const float mass = 0.4 ; //0.03;

  // Implement mass-spring-damper
  // 1) calculate dt
  unsigned long current = millis();
  float dt = (float) (current - prev)/ 10000;

  // 2) calculate position and velocity of the mass
  float a = - hapkit.getForceFeedback()/mass;
  float v = a*dt;
  float x = v*dt;

  // 3) calculate relative position and velocity
  float relativeVelocity = hapkit.getVelocity() - v;
  //float relativePosition = hapkit.getPosition() - x;
  relativePosition = hapkit.getPosition() - x;

  // write the position of the character
  //Serial.print("\trelativePosition:");Serial.println(relativePosition);
  
  // 4) calculate force
  //float force = (-stiffness * relativePosition) - (damping * relativeVelocity);
  force = (-stiffness * relativePosition) - (damping * relativeVelocity);
  float totalForce = force + incomingWind;

  // 5) set force feedback
  hapkit.setForceFeedback(totalForce);

  // update the time variables
  prev = current;
}

//Hapkit hapkit(&virtualCoupling, &shiftingWindow);
Hapkit hapkit(&virtualCoupling);

void setup() {
  Serial.begin(9600);
  hapkit.setKinematicConstant(4.13);
  hapkit.begin();
}

void loop() {
  hapkit.update();
  
  // print every 50 ms
  static int tPrev = millis();
  int tCurrent = millis();
  static constexpr int printPeriod = 50;

  // read the incoming wind:
  incomingWind = (float) Serial.read();

  if (abs(tCurrent - tPrev) > printPeriod) {
    Serial.print("\trel_position:");Serial.println(relativePosition);
    //Serial.print("\tforce_feedback:");Serial.print(force);
    //Serial.print("\twind:");Serial.print(incomingWind);
    //Serial.print("\tforce_feedback_with_wind:");Serial.println(hapkit.getForceFeedback());  
    tPrev = tCurrent;
  }
}
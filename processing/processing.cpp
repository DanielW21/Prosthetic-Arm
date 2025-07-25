#include <Servo.h>

Servo myservo1;
const int servoPin = 11;
const int vInPin = A0;

// Tracking Variables
int currentAngle = 0;

// Dynamic Variables
int thresholdRaw = 614; 

int direction = 1; //increasing = 1, decreasing = -1

bool isAboveThreshold = false;
bool wasAboveThreshold = false;

unsigned long pulseStartTime = 0;
unsigned long lastStepTime = 0;

void setup() {
  Serial.begin(9600);
  myservo1.attach(servoPin);
  myservo1.write(currentAngle);
  Serial.println("Servo initialized to 0 degrees.");
}

void loop() {
  int analogValue = analogRead(vInPin);
  float voltage = analogValue * (5.0 / 1023.0);
//
//  Serial.print("Analog V_in: ");
//  Serial.print(analogValue);
//  Serial.print(" (");
//  Serial.print(voltage, 2);
//  Serial.println(" V)");

  isAboveThreshold = analogValue > thresholdRaw;
  unsigned long currentTime = millis();

  if (isAboveThreshold && !wasAboveThreshold) {
    pulseStartTime = currentTime;
    lastStepTime = currentTime;
    Serial.println("Pulse started.");
  }

  if (isAboveThreshold) {
    unsigned long pulseDuration = currentTime - pulseStartTime;

    //high > 200ms, step every 200ms
    if (pulseDuration >= 1000 && currentTime - lastStepTime >= 200) {
      currentAngle += 5 * direction;

      // Clamp angle
      currentAngle = constrain(currentAngle, 0, 180);

      myservo1.write(currentAngle);
      lastStepTime = currentTime;

      Serial.print("Live step! New angle: ");
      Serial.println(currentAngle);
    }
  }

  if (!isAboveThreshold && wasAboveThreshold) {
    unsigned long totalPulse = currentTime - pulseStartTime;
    Serial.print("Pulse ended. Duration: ");
    Serial.print(totalPulse);
    Serial.println(" ms");

    if (totalPulse >= 200 && totalPulse <= 1200) {
      direction *= -1;
      Serial.print("Direction reversed! Now: ");
      Serial.println((direction == 1) ? "increasing" : "decreasing");
    }
  }

  wasAboveThreshold = isAboveThreshold;

  delay(100); 
}

//  Sharp GP2xx IR sensor
#include <SoftwareSerial.h>
#include <Servo.h>

SoftwareSerial MySerial(4, 5); // RX, TX
Servo MyServo;

int count = 0;

void setup(){
  MyServo.attach(9);
  Serial.begin(9600);
  MySerial.begin(9600);
}

void loop(){

  int sensorValue = analogRead(A0);                    //sensor input
  float voltage = sensorValue*5.0/1024;             //voltage mapping
  float distance =27.15*pow(voltage,-1.179);    //by curve fitting

  if(distance < 60) {
    count++;
    if(count==1) Serial.print('d');
  }
  
  while(MySerial.available()) {
    int data = MySerial.read();
    if(data == 111) {
      for (int pos = 0; pos <= 180; pos += 1) {
        MyServo.write(pos);
        delay(5);
      }
      delay(10000);
      for(int pos = 180; pos>=0; pos-=1) {
        MyServo.write(pos);
        delay(5);
      }
    }
  }

  while(Serial.available()) {
    int data = Serial.read();
    if(data == 111) {
      for (int pos = 0; pos <= 180; pos += 1) {
        MyServo.write(pos);
        delay(5);
      }
      delay(10000);
      for(int pos = 180; pos>=0; pos-=1) {
        MyServo.write(pos);
        delay(5);
      }
    }
  }  
}

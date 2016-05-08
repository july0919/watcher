//  Sharp GP2xx IR sensor
void setup(){
  Serial.begin(9600);
}

void loop(){
  int sensorValue = analogRead(A0);                    //sensor input
  float voltage = sensorValue*5.0/1024;             //voltage mapping
  float distance =27.15*pow(voltage,-1.179);    //by curve fitting
  
  Serial.println(distance);
//  Serial.println("cm");
  delay(1000);
}

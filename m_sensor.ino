#include<Servo.h>
Servo servo1;
Servo servo2;
int sensor = A3;
int motor_ac = 12;
int sensor_value;
int pos;
char command;
void setup()
{
  Serial.begin(9600);
  pinMode(sensor, INPUT);
  pinMode(motor_ac, OUTPUT);
  digitalWrite(motor_ac,LOW);
  servo1.attach(9);
  servo2.attach(10);
}
void loop()
{
  sensor_value = analogRead(sensor);
  Serial.println(sensor_value); 
  if (Serial.available() > 0)
  {
    command = Serial.read();
    regular();
    switch (command)
    {
      case 'C' : overwrite();
      break;
    }
  }
  else 
  regular();
}

void regular()
{
  if (600 < sensor_value < 1000)
  {
    digitalWrite(motor_ac, LOW);
  }
  else if (sensor_value < 600)
  {
    digitalWrite(motor_ac, HIGH);
    for (pos = 0; pos <= 180; pos++)
    {
      servo1.write(pos);
      servo2.write(pos);
    }
    delay(1000);
    for (pos = 180; pos >= 0; pos--)
    {
      servo1.write(pos);
      servo2.write(pos);
    }
  }
}

void overwrite()
{
  digitalWrite(motor_ac, LOW);
  delay(5000);
  digitalWrite(motor_ac, HIGH);
}   

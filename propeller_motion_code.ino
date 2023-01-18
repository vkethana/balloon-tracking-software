// Created during 2022 Summer STEM Research Internship at Gavilan College (Vijay Kethanaboyina, Bryce Mankovsky, and Jonathan Tessmann)

int motor1pin1 = 3;
int motor1pin2 = 4;
int motor2pin1 = 5;
int motor2pin2 = 6;

void setup() {
  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);
  pinMode(motor2pin1, OUTPUT);
  pinMode(motor2pin2, OUTPUT);
}

void loop() { 
  digitalWrite(motor1pin1, HIGH);
  digitalWrite(motor1pin2, LOW);
  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);
  
  delay(30000); // 30 seconds

  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, LOW);
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, LOW);
  
  delay(99999999999999999999); // delay forever, hit reset button to restart 
}

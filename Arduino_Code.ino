#define left_motor_forward 8
#define left_motor_backward 9
#define left_motor_pwm 10
#define right_motor_pwm 11
#define right_motor_forward 12
#define right_motor_backward 13
char c;
int iRPin=A0;
int bazarPin=7;
int sensor;
int sen;

void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);
  pinMode(left_motor_forward,OUTPUT);
  pinMode(left_motor_backward,OUTPUT);
  pinMode(right_motor_forward,OUTPUT);
  pinMode(right_motor_backward,OUTPUT);
  pinMode(bazarPin,OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available())
  {
    c=Serial.read();
    if(c=='f')
    forward();
    else if(c=='b')
    backward();
    else if(c=='l')
    left_turn();
    else if(c=='r')
    right_turn();
    else if(c=='s')
    {
      Stop();
      delay(10);
      IRSENSOR();
      
    }
    if(c=='x')
    bazar();
  }

}
void forward()
{
  Serial.println("the bot will move forward");
  digitalWrite(left_motor_forward,1);
  digitalWrite(right_motor_forward,1);
  digitalWrite(left_motor_backward,0);
  digitalWrite(right_motor_backward,0);
  analogWrite(left_motor_pwm,250);
  analogWrite(right_motor_pwm,250);
  delay(100);
  Stop();
  
}
void backward()
{
  Serial.println("the bot will move backward");
  digitalWrite(left_motor_backward,1);
  digitalWrite(right_motor_backward,1);
  digitalWrite(left_motor_forward,0);
  digitalWrite(right_motor_forward,0);
  analogWrite(left_motor_pwm,250);
  analogWrite(right_motor_pwm,250);
  delay(100);
  Stop();
}
void right_turn()  //hard right turn
{
  Serial.println("the bot will take a hard right turn");
  digitalWrite(left_motor_forward,1);
  digitalWrite(right_motor_forward,0);
  digitalWrite(left_motor_backward,0);
  digitalWrite(right_motor_backward,1);
  analogWrite(left_motor_pwm,200);   
  analogWrite(right_motor_pwm,100);
  delay(60);   //you may have to vary the delay for perfect right turn..
  Stop();
}
void left_turn()    //hard left turn
{
  Serial.println("the bot will take a hard left turn");
  digitalWrite(left_motor_forward,0);
  digitalWrite(right_motor_forward,1);
  digitalWrite(left_motor_backward,1);
  digitalWrite(right_motor_backward,0);
  analogWrite(left_motor_pwm,100);
  analogWrite(right_motor_pwm,200);
  delay(60);   //you may have to vary the delay for perfect right turn..
  Stop();
}
void Stop()
{
  Serial.println("the bot will stop");
  analogWrite(left_motor_pwm,0);
  analogWrite(right_motor_pwm,0);
}
void IRSENSOR()
{
  sensor=analogRead(iRPin);
 sen=sensor/4;
  if(sen<255)
  {
    digitalWrite(bazarPin,HIGH);
    delay(3000);
    digitalWrite(bazarPin,LOW);
    delay(3000);
  }
}

void bazar()
{
  digitalWrite(bazarPin,HIGH);
  delay(5000);
  digitalWrite(bazarPin,LOW);
  delay(5000);
}



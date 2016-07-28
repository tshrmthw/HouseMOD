/*
 * PIR sensor tester
 */
 
int myPins[] = {0,1,2,3,4};
int sensorState[] = {HIGH,HIGH,HIGH,HIGH,HIGH};
int val[] = {0,0,0,0,0};
char* sensorStrings[] = {"Sensor 1 Triggered","Sensor 2 Triggered","Sensor 3 Triggered","Sensor 4 Triggered","Sensor 5 Triggered"} ;

void setup() {
   for(int i = 0; i < 5; i = i + 1){
    pinMode(myPins[i], INPUT_PULLUP);
  }
  Serial.begin(9600);
}
 
void loop(){
  for(int i = 0; i < 5; i = i + 1) {
    val[i] = digitalRead(myPins[i]);  // read input value
    if (val[i] == LOW) {            // check if the input is HIGH
      if (sensorState[i] == HIGH) {
      Serial.println("{'id':48,'type':3}");
      sensorState[i] = LOW;
    }
    else{
      if (sensorState[i] == LOW){
        sensorState[i] = HIGH;
      }
    }
    }
    delay(10000);
}
}

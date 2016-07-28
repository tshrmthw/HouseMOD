/*
 * PIR sensor tester
 */
 
int myPins[] = {1,2,3};
int sensorState[] = {LOW,LOW,LOW,LOW,LOW};
int val[] = {0,0,0,0,0};
char* sensorStrings[] = {"{'id':46,'type':3}","{'id':45,'type':3}","{'id':47,'type':3}"} ;

void setup() {
   for(int i = 0; i < 5; i = i + 1){
    pinMode(myPins[i], INPUT_PULLUP);
  }
  Serial.begin(9600);
}
 
void loop(){
  for(int i = 0; i < 3; i = i + 1) {
    val[i] = digitalRead(myPins[i]);  // read input value
    if (val[i] == HIGH) {            // check if the input is LOW
      if (sensorState[i] == LOW) {
      Serial.println(sensorStrings[i]);
      sensorState[i] = HIGH;
    }
    else{
      if (sensorState[i] == HIGH){
        sensorState[i] = LOW;
      }
    }
    }
    delay(100);
}
}

/*
 * PIR sensor tester
 */
 
int inputPin = 2;               // choose the input pin (for PIR sensor)
int remoteInputPin = 3;               // choose the input pin (for PIR sensor)
int pirState = LOW;             // we start, assuming no motion detected
int remotePirState = LOW;
int val = 0;                    // variable for reading the pin status
int remoteVal = 0;
 
void setup() {
  pinMode(inputPin, INPUT_PULLUP);     // declare sensor as input
  pinMode(remoteInputPin, INPUT_PULLUP);
  Serial.begin(9600);
}
 
void loop(){
  val = digitalRead(inputPin);  // read input value
  remoteVal = digitalRead(remoteInputPin);  // read input value
  if (val == HIGH) {            // check if the input is HIGH
    if (pirState == LOW) {
      // we have just turned on
      Serial.println("{'id':45,'type':3}");
      // We only want to print on the output change, not state
      pirState = HIGH;
    }
  } else {
    if (pirState == HIGH){
      // We only want to print on the output change, not state
      pirState = LOW;
    }
  }
    if (remoteVal == HIGH) {            // check if the input is HIGH
    if (remotePirState == LOW) {
      // we have just turned on
      Serial.println("{'id':46,'type':3}");
      // We only want to print on the output change, not state
      remotePirState = HIGH;
    }
  } else {
    if (remotePirState == HIGH){
      // We only want to print on the output change, not state
      remotePirState = LOW;
    }
  }
}

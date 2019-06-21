
/* AT Command Read Example
Author: Leo
Copyright 2019, github/LeoAndGit>
*/

String inputString = "";         // a string to hold incoming data
float frequency = 0;

void setup() {
  // initialize the digital pin as an output.
  pinMode(PB0, OUTPUT);
  Serial.begin(9600); 
  Serial.setTimeout(1000); 
  inputString.reserve(80); // allows you to allocate a buffer in memory for manipulating Strings
  digitalWrite(PB0,HIGH);
  Serial.println("AT command Read Example:");
  }

void loop() {
 if (Serial.available() > 0) {
  inputString = String(Serial.readStringUntil(10));//search for \n
  	if(inputString.endsWith(String('\r'))){
  		if (inputString=="AT\r"){
  			Serial.println("OK");
  		} 
  		else if(inputString=="AT+START\r"){
  			Serial.println("OK");
  		} 
  		else if(inputString=="AT+STOP\r"){
  			Serial.println("OK");
  		}
  		else if(inputString=="AT+VERSION\r"){
  			Serial.println("AT command Read Example");
  			Serial.println("OK");
  		} 
  		else if(inputString.substring(0,8)=="AT+FREQ="){
  			String strFreq =  inputString.substring(8,13);
  			frequency = strFreq.toFloat();
  			Serial.println(frequency);
  			Serial.println("OK");
  		}
  		else{
  			Serial.println("Error command");
  		}
  	}
  	else{
  		Serial.println("Error end check");
  	}
  
 }

}

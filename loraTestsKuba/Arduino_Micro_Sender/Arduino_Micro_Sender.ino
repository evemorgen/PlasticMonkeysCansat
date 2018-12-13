`#include <LoRa.h> 

#define BAND 433E6

int counter = 0;
int delayTime = 100;

void setup() {
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  Serial.begin(9600);
  Serial.println("Hello Arduino Lora Sender");
  if (!LoRa.begin(BAND)){
    Serial.println("LoRa Initialization failed:");  
    while(1);
  }
  LoRa.setSpreadingFactor(7);
  LoRa.setTxPower(20);
  Serial.println("LoRa initialization successful");
}

void loop() {
  digitalWrite(13, HIGH);
  Serial.print("Sending packet: ");
  Serial.println(counter);

  LoRa.beginPacket();
  LoRa.print(counter);
  LoRa.print(" abababababababababababababababababababababababababababababab");
  LoRa.endPacket();
  counter++;
  
  delay(delayTime/2);
  digitalWrite(13, LOW);
  delay(delayTime/2);
}

#include <LoRa.h> 
int counter = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  Serial.begin(9600);
  Serial.println("Hello Arduino Lora Sender");
  if (!LoRa.begin(433E6)){
    Serial.println("LoRa Initialization failed:");  
    while(1);
  }
  Serial.println("LoRa initialization successful");
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(13, HIGH);
  Serial.print("Sending packet: " + counter);

  LoRa.beginPacket();
  LoRa.print("Hello LoRa: ");
  LoRa.print(counter);
  LoRa.endPacket();

  counter++;
  delay(100);
  digitalWrite(13, LOW);
  delay(2000);
}

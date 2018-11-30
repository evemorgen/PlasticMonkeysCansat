#include <LoRa.h> 
#include <LED.h>
int counter = 0;
LED led (13);

void setup() {
  // put your setup code here, to run once:
  led.off();
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
  led.on();
  Serial.print("Sending packet: " + counter);

  LoRa.beginPacket();
  LoRa.print("Hello LoRa: ");
  LoRa.print(counter);
  LoRa.endPacket();

  counter++;
  delay(100);
  led.off();
  delay(2000);
}

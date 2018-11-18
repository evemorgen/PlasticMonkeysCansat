#include <LoRa.h>
int counter = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  Serial.begin(9600);
  /*while (!Serial){
    delay(200);
  }*/
  Serial.println("Hello Arduino Lora Sender");
  int c=0;
  while (!LoRa.begin(433E6)){
    delay(200);
    c++;
    Serial.println("LoRa Initialization failed:");  
    Serial.print(c);
  }
  Serial.println("LoRa setup successful");
  
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(13, HIGH);
  Serial.print("Sending packet: ");
  Serial.println(counter);

  LoRa.beginPacket();
  LoRa.print("Hello LoRa: ");
  LoRa.print(counter);
  LoRa.endPacket();

  counter++;
  delay(100);
  digitalWrite(13, LOW);
  delay(2000);
}

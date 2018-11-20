#include <LoRa.h>
int counter = 0;

String rssi ;
String packSize ;
String packet = "ABCDEFGHIJKLMNO";
String sentPacket ;

bool success;

void readPacket(int packetSize) {
  packet ="";
  packSize = String(packetSize,DEC);
  for (int i = 0; i < packetSize; i++) {
    packet += (char) LoRa.read();
  }
  rssi = "ArdRSSI " + String(LoRa.packetRssi(), DEC) ;
  Serial.print("Received Packet: ");
  Serial.println(packet);
}

void sendPacket(){
   if (success) {
     sentPacket = "";
     sentPacket += "Ra02: ";
     sentPacket += "Tms ";
     for (int i = 5; i < 12; i++){
        sentPacket += packet[i]; 
     }  
     sentPacket += " C:";
     sentPacket += String(counter);
   } else {
     sentPacket = "";
     sentPacket += "Ra02: ";
     sentPacket += "READ FAIL";
     sentPacket += " C:";
     sentPacket += String(counter);
   }
   Serial.println("");
   Serial.print("Sending packet: ");
   Serial.println(sentPacket);

   LoRa.beginPacket();
   LoRa.print(sentPacket);
   LoRa.endPacket();
}

void setup() {
  // put your setup code here, to run once:
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  Serial.begin(9600);
  while (!Serial){
    delay(200);
  }
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
  delay(70);

  sendPacket();

  counter++;
  digitalWrite(13, LOW);
  delay(15);
  int time0 = millis();
  int window = 3000;
  success = false;
  while (window > 0){
    window = 3000 - (millis()-time0);
    int packetSize = LoRa.parsePacket();
    if (packetSize) {
      readPacket(packetSize);
      success = true;
      break;
    }
    delay(5);
  }
  if (!success) Serial.println("Read falied.");
  if (window > 0) delay(window);
}

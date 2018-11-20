#include <LoRa.h> //External library by Sandeep Mistry https://github.com/sandeepmistry/arduino-LoRa

int counter = 0; //Counting packets

String packSize ;
String packet = "ABCDEFGHIJKLMNO"; //placeholder for the first packet to be received
String sentPacket ; //packet to be sent

bool success; //was a packet recieved during  slave-talk frame?

void readPacket(int packetSize) {
  //Reads last packet from radio socket
  packet ="";
  for (int i = 0; i < packetSize; i++) {
    packet += (char) LoRa.read();
  }
  Serial.print("Received Packet: ");
  Serial.println(packet);
}

void sendPacket(){
   //Transmits packet with following properties
   //Returns number sent by TTGO
   sentPacket = "";
   sentPacket += "Ra02: ";
   if (success) {
     sentPacket += "Tms ";
     for (int i = 5; i < 12; i++){
       sentPacket += packet[i]; 
     }  
   } else {
     sentPacket += "READ FAIL";
   }
   sentPacket += " C:";
   sentPacket += String(counter);
 
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
  /*while (!Serial){ //use to wait for serial monitor activation
    delay(200);
  }*/
  Serial.println("Serial init OK");
  if (!LoRa.begin(433E6)){
    Serial.println("LoRa Initialization failed:");  
    while(1);
  }
  Serial.println("LoRa setup successful");
}

void loop() {
  digitalWrite(13, HIGH); //Turn on LED
  delay(70);

  sendPacket();

  counter++;
  digitalWrite(13, LOW); //Turn off LED
  delay(15);
  int time0 = millis();
  int window = 3000;    //Slave responce tmie window
  success = false;
  while (window > 0){   //Listen for packs
    window = 3000 - (millis()-time0);
    int packetSize = LoRa.parsePacket();
    if (packetSize) {
      readPacket(packetSize);
      success = true;
      break;
    }
  }
  if (!success) Serial.println("Read falied.");
  if (window > 0) delay(window); //Wait with TX till end of window
}

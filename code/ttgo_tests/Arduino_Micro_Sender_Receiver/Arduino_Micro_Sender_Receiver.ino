#include <LoRa.h> //External library by Sandeep Mistry https://github.com/sandeepmistry/arduino-LoRa

int counter = 0; //Counting packets

String packSize;
String packet; //received packet
String sentPacket; //packet to be sent

int packetsSent = 0;
int packetsRcvd = 0;
int successRatio = 100;

bool success; //was a packet recieved during  slave-talk frame?

void readPacket(int packetSize) {
  //Reads last packet from radio socket
  packet ="";
  for (int i = 0; i < packetSize; i++) {
    packet += (char) LoRa.read();
  }
  Serial.print("Received Packet: ");
  Serial.println(packet);
  packetsRcvd++;
}

void sendPacket(){
   //Transmits packet with following properties
   //Returns number sent by TTGO
   sentPacket = "";
   sentPacket += "ID: ";
   if (success) {
     for (int i = 4; i <= 7; i++){
       sentPacket += packet[i]; 
     }  
   } else {
     sentPacket += "FAIL";
   }
   
   successRatio = packetsSent != 0 ? ((int)(100*packetsRcvd/packetsSent)) : 0;
   sentPacket += " Succ: ";
   sentPacket += successRatio;   
   sentPacket += "% Sent: ";
   sentPacket += packetsSent;
   sentPacket += " Rcvd: ";
   sentPacket += packetsRcvd;
   
   Serial.println("");
   Serial.print("Sending packet: ");
   Serial.println(sentPacket);

   LoRa.beginPacket();
   LoRa.print(sentPacket);
   LoRa.endPacket();
   packetsSent++;
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
  int window = 3000;    //Slave responce time window
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

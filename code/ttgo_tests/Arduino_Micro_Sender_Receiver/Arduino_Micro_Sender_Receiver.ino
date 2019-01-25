#include <LED.h>
#include <LoRa.h> //External library by Sandeep Mistry https://github.com/sandeepmistry/arduino-LoRa
int counter = 0; //Counting packets

String packet; //received packet
String sentPacket;

long packetsSent = 0;
long packetsRcvd = 0;
int successRatio = 100;

bool success; //was a packet recieved during  slave-talk frame?

LED led = LED(13);

void readPacket(int packetSize) {
  //Reads last packet from radio socket
  packet = LoRa.readString();
  Serial.println("Received Packet: " + packet);
  packetsRcvd++;
}

void sendPacket(){
   //Transmits packet with following properties
   //Returns number sent by TTGO
   String sentPacket = "";
   sentPacket += "ID: ";
   if (success) {
     for (int i = 4; i <= 8; i++){
       sentPacket += packet[i]; 
     }  
   } else {
     sentPacket += "FAIL";
   }
   
   successRatio = packetsSent != 0 ? 100*packetsRcvd/packetsSent : 0;
   sentPacket += " Succ: " + String(successRatio);
   sentPacket += "%\nSent: " + String(packetsSent);
   sentPacket += " Rcvd: " + String(packetsRcvd);
   
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
  led.off();
  Serial.begin(9600);
  Serial.println("Serial init OK");
  if (!LoRa.begin(433E6)){
    Serial.println("LoRa Initialization failed!");  
    while(1);
  }
  Serial.println("LoRa init successful");
  LoRa.setSpreadingFactor(7);
  LoRa.setTxPower(20);
  Serial.println("LoRa init successful");
}

void loop() {
  led.on();
  delay(10);

  sendPacket();

  counter++;
  led.off();
  int time0 = millis();
  int window = 200;    //Slave responce time window
  success = false;
  while (window > 0){   //Listen for packs
    window = 200 - (millis()-time0);
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

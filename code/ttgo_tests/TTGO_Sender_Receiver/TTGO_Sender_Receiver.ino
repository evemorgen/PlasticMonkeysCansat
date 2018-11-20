#include <LoRa.h> //https://github.com/sandeepmistry/arduino-LoRa
#include <SPI.h>  
#include <Wire.h>
#include "SSD1306.h" 

#define SCK     5    // GPIO5  -- SX1278's SCK
#define MISO    19   // GPIO19 -- SX1278's MISO
#define MOSI    27   // GPIO27 -- SX1278's MOSI
#define SS      18   // GPIO18 -- SX1278's CS
#define RST     14   // GPIO14 -- SX1278's RESET
#define DI0     26   // GPIO26 -- SX1278's IRQ(Interrupt Request)
#define BAND    433E6// 433 MHz Freq

SSD1306 display(0x3c, 4, 15);
String rssi ;
String packSize ;
String packet ;
String sentPacket ;

int packetsSent = 0;
int packetsRcvd = 0;
float successRatio = 100;

void displayLoraData(){
  display.clear();
  display.drawString(0 , 15 , "Bytes: " + packSize);
  display.drawStringMaxWidth(0 , 33 , 128, packet);
  display.drawString(0, 0, "RSSI: "+ rssi);  
  display.drawString(50, 0, "TX: "+ String(packetsSent));
  display.drawString(85, 0, "RX: "+ String(packetsRcvd));
  display.drawString(50, 15, "Succ: "+ String(successRatio)+"%");
  display.display();
}

void readPacket(int packetSize) {
  //Reads packet from radio socket
  packet ="";
  packSize = String(packetSize,DEC);
  for (int i = 0; i < packetSize; i++) {
    packet += (char) LoRa.read();
  }
  rssi = String(LoRa.packetRssi(), DEC) ;
  packetsRcvd++;
  displayLoraData();
}

void sendPacket(){
  //Sends LoRa packet containing a number (milliseconds since start)
  sentPacket = "TTGO: ";
  sentPacket += String(millis());
  sentPacket += " ms";
  
  LoRa.beginPacket();
  LoRa.print(sentPacket);
  LoRa.endPacket();

  packetsSent++;
  
  display.drawString(0, 44, "Sent: "+sentPacket);
  display.display();
}

void setup() {
  pinMode(16,OUTPUT); //OLED reset pin

  //Reset OLED
  digitalWrite(16, LOW); 
  delay(50); 
  digitalWrite(16, HIGH);

  //Initialize OLED
  display.init(); 
  display.drawString(0, 0, "Display Init OK");

  //Initialize Serial
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Serial Initialization Successful");
  display.drawString(0, 20, "Serial Init OK");

  //Initialize LoRa
  SPI.begin(SCK,MISO,MOSI,SS);
  LoRa.setPins(SS,RST,DI0);  
  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    display.drawString(0, 40, "LoRa Init FAIL");
    display.display();
    while (1);
  }
  //LoRa.receive();
  Serial.println("Init OK");
  display.drawString(0, 40, "LoRa Init OK");
  display.display();
  
  delay(3000);
  display.clear();
}

void loop() {
  int packetSize = LoRa.parsePacket();
  while(!packetSize){
    packetSize = LoRa.parsePacket();
    delay(20);
  };
  if (packetSize) readPacket(packetSize);
  delay(300);
  sendPacket();
  successRatio = ((int)(1000*packetsRcvd/packetsSent))/10;
}

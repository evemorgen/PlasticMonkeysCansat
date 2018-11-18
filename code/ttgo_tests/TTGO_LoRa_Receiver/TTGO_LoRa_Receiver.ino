#include <LoRa.h>
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



void displayLoraData(){
  display.clear();
  display.drawString(0 , 15 , "Received "+ packSize + " bytes");
  display.drawStringMaxWidth(0 , 26 , 128, packet);
  display.drawString(0, 0, rssi);  
  display.display();
}

void readPacket(int packetSize) {
  packet ="";
  packSize = String(packetSize,DEC);
  for (int i = 0; i < packetSize; i++) {
    packet += (char) LoRa.read();
  }
  rssi = "RSSI " + String(LoRa.packetRssi(), DEC) ;
  displayLoraData();
}

void setup() {
  pinMode(16,OUTPUT);

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
    while (1);
  }
  LoRa.receive();
  Serial.println("Init OK");
  display.drawString(0, 40, "LoRa Init OK");
  display.display();
  
  delay(5000);
}

void loop() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) readPacket(packetSize);
  delay(10);
}

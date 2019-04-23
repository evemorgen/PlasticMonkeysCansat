#include <SPI.h>
#include <Wire.h>
#include <RH_RF95.h>
#include "SSD1306.h"

#define RFM95_CS 18
#define RFM95_RST 14
#define RFM95_INT 26
#define RF95_FREQ 434.2

RH_RF95 rf95(RFM95_CS, RFM95_INT);

SSD1306 display(0x3c, 4, 15);

uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
uint8_t len = sizeof(buf);

RH_RF95::ModemConfig modem_config = {72, 78, 4};

void setup()
{
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);
  pinMode(16, OUTPUT); //OLED reset pin
  digitalWrite(16, LOW); //Reset OLED
  delay(50);
  digitalWrite(16, HIGH);

  while (!Serial);
  Serial.begin(9600);
  delay(100);
  Serial.println("Serial initialized");
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  while (!rf95.init()) {
    Serial.println("LoRa init failed");
    while (1);
  }
  
  rf95.setFrequency(434.2);
  rf95.setTxPower(20);
  rf95.setSpreadingFactor(7);
  rf95.setCodingRate4(5);
  rf95.setPreambleLength(12);
  rf95.setSignalBandwidth(125000);

  display.init();
  display.clear();
  display.drawString(0, 20, "INIT OK");
  display.display();
  Serial.print(rf95.printRegisters());
  delay(1000);
  Serial.println("INIT OK");
}

int packet_length = 25;
int send_length = 0;
bool rcv_success = false;
int packetID = 0;
String lastPacket = "";
uint8_t lastBuf[RH_RF95_MAX_MESSAGE_LEN];
int csum = 0;

String createPacket() {
  String p = "";
  csum = 0;
  int len = Serial.available();
  if (!len){
    p += "B";
    send_length = 1;
  } else {
    for (int i = 0; i < len; i++){
      p += (char)Serial.read();
    }
    send_length = len;
    
    if (send_length != 1) { //please excuse this
      for (int i = 0; i < len-1; i++){
        csum += ((char)p[i]*(char)p[i+1] % 991);
      }
      csum = csum % 255; //it works fine though
    }
  }
  
  return p;
}


void loop()
{
  if (rf95.available()) {
    if (rf95.recv(buf, &len)) {
      int rssi = rf95.lastRssi();
      String received = String((char*)buf);
      rcv_success = true;
      Serial.write(buf, 25);
      display.clear();
      
      String message = createPacket();

      display.drawString(50, 0, String(csum));
      display.drawString(0 , 15, "RX: " + received);
      display.drawString(0, 0, "RSSI: " + String(rssi));
      display.drawString(0, 40, "TX: " + message);
      display.display();
      delay(80);

      uint8_t data[50] = {0};
      for (int i = 0; i < send_length; i++) {
        data[i] = (uint8_t) message[i];
      }
      data[send_length] = csum;

      rf95.send(data, send_length+1); //sizeof(data)
      rf95.waitPacketSent();
    }
    else
    {
      Serial.println("Receive failed");
    }
  } 
}

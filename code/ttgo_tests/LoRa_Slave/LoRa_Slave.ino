// This program sends a response whenever it receives the "INF" mens
//
// Copyright 2018 Rui Silva.
// This file is part of rpsreal/LoRa_Ra-02_Arduino
// Based on example Arduino9x_RX RADIOHEAD library
// It is designed to work with LORA_SERVER

#include <SPI.h>
#include <Wire.h>
#include <RH_RF95.h>
#include "SSD1306.h"

#define RFM95_CS 18
#define RFM95_RST 14
#define RFM95_INT 26

// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 433.0

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

// Blinky on receipt
#define LED 13

//OLED
SSD1306 display(0x3c, 4, 15);

uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
//uint8_t buf[65];
uint8_t len = sizeof(buf);

void setup()
{
  pinMode(LED, OUTPUT);
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  pinMode(16, OUTPUT); //OLED reset pin

  //Reset OLED
  digitalWrite(16, LOW);
  delay(50);
  digitalWrite(16, HIGH);

  while (!Serial);
  Serial.begin(9600);
  delay(100);
  Serial.println("Serial initialized");
  Serial.println(len);
  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    digitalWrite(LED, HIGH);
    while (1);
  }

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    digitalWrite(LED, HIGH);
    while (1);
  }

  rf95.setTxPower(18);
  rf95.setSpreadingFactor(7);
  rf95.setCodingRate4(5);
  rf95.setPreambleLength(12);
  //rf95.setLowDatarate();
  //!!rf95.setPayloadCRC(false);

  //rf95.setModemConfig(RH_RF95::Bw125Cr45Sf128);
  Serial.println("START");

  display.init();
  display.clear();
  display.drawString(0, 20, "INIT OK");
  display.display();
  //Serial.print(rf95.printRegisters());
  delay(4000);
  Serial.println("INIT OK");
}

int packet_length = 20;
bool rcv_success = false;
int packetID = 0;

String createPacket() {
  
  /*String p = "";
  p += "ID: ";
  p += String(packetID);
  p += " ABCDEFGHIJKL";

  packetID += 1;
  return p;*/


  //PACKET PROTOCOL:
  //L: led (L1 - on, L0 - off) 
  //B: buzzer
  //
  //
  //
  //
  //
  //
  String p = "";
  int len = Serial.available();
  if (!len){
    p += "---------------";
  } else {
    for (int i = 0; i < len; i++){
      p += (char)Serial.read();
    }
    for (int i = len; i < 20; i++){
      p += "-";
    }
  }
  return p;
}

uint8_t *_buf;

void loop()
{
  if (rf95.available()) {
    //Serial.println("Available");
    
    if (rf95.recv(buf, &len)) {
      digitalWrite(LED, HIGH);

      int rssi = rf95.lastRssi();
      String received = String((char*)buf);
      rcv_success = true;

      String message = createPacket();

      Serial.print("RX: ");
      Serial.print(received);
      Serial.print(" RSSI: ");
      Serial.print(rssi, DEC);
      Serial.print(" Time: ");
      Serial.print(millis());
      Serial.println(" ");

      display.clear();
      display.drawString(0 , 15, "RX: " + received);
      display.drawString(0, 0, "RSSI: " + String(rssi));
      display.drawString(0, 40, "TX: " + message);
      display.display();
      delay(80);
      Serial.println("TX: " + message);

      uint8_t data[50] = {0};

      for (int i = 0; i < packet_length; i++) {
        data[i] = (uint8_t) message[i];
      }

      //uint8_t data[] = "Hello TTGO whatever";

      rf95.send(data, packet_length); //sizeof(data)
      rf95.waitPacketSent();
        
      digitalWrite(LED, LOW);
    }
    else
    {
      Serial.println("Receive failed");
    }
  }
}

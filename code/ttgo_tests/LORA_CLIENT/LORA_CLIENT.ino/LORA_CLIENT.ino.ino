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
#define RF95_FREQ 434.0

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

// Blinky on receipt
#define LED 13

//OLED
SSD1306 display(0x3c, 4, 15);

void setup() 
{
  pinMode(LED, OUTPUT);     
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  pinMode(16,OUTPUT); //OLED reset pin

  //Reset OLED
  digitalWrite(16, LOW); 
  delay(50); 
  digitalWrite(16, HIGH);

  while(!Serial);
  Serial.begin(9600);
  delay(100);
  Serial.println("Serial initialized");
  
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
  rf95.setSpreadingFactor(12);
  Serial.println("START");

  display.init();
  display.clear();
  display.drawString(0, 20, "INIT OK");
  display.display();
  delay(4000);
  Serial.println("Here");
}
    
uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];    
uint8_t len = sizeof(buf);

void loop()
{
  if (rf95.available()){    
    Serial.println("Available");
    if (rf95.recv(buf, &len)){
      digitalWrite(LED, HIGH);
      //RH_RF95::printBuffer("Got: ", buf, len);
      
      int rssi = rf95.lastRssi();
      String received = (char*)buf;

      String message = "Hello TTGO whatever";
      int msglen = 19;
      
      Serial.print("Received:  ");
      Serial.println(received);
      Serial.print("RSSI: ");
      Serial.println(rssi, DEC);

      display.clear();
      display.drawString(0 , 15, "RX: " + received);
      display.drawString(0, 0, "RSSI: " + String(rssi));
      display.drawString(0, 40, "TX: " + message);
      display.display();
      delay(1000);
      Serial.println("TX: " + message);
      
      uint8_t data[] = "Hello TTGO whatever";
      rf95.send(data, msglen); //sizeof(data)
      rf95.waitPacketSent();
      digitalWrite(LED, LOW);
    }
    else
    {
      Serial.println("Receive failed");
    }
  }
}

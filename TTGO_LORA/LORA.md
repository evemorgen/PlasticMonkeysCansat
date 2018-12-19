# LoRa w/ TTGO

Hello, here are some notes about our RaO2 working with TTGO.

## TTGO SETUP

Firstly - our TTGO from Germany is actually called Heltec WiFi LoRa 32

To start working with it you need to add some libraries, it is shown in steps below:

#### Step 1
Erase all old ESP32 Libraries that you've installed before. If you haven't you can skip this step.

#### Step 2
Jump to Arduino IDE, go to File > Preferences > Additional Board Manager URLs, add this line:
`https://dl.espressif.com/dl/package_esp32_index.json`

#### Step 3
Jump to Tools > Boards > Board Manager and search ESP32, next download:
`esp32 by Espressif Systems`

#### Step 4
Go to Library Manager (Open Sketch > Include Library > Manage Libraries) and install:
`LoRa by Sandeep Mistry`

#### Step 5
Install another library from Libraries Manager:
`U8g2`

Alternative Link: [U8g2](https://github.com/olikraus/u8g2)

#### Step 6

Go to Boards and select:
`Heltec_WIFI_LoRa_32`

#### That's it!

## LORA NOTES

In my configuration (Arduino Micro with Ra02 as a TX, Heltec Board as a receiver) it works with best results with:

#### TX
```LoRa.setSpreadingFactor(7)
LoRa.setTxPower(20); //TX Power
int delayTime = 100; //Time between sending packets
```

Coding Rate and Spreading Factor are responsible for data transfer speed. However Coding Rate is set to the best value
By default, Spreading factor is the better the lower. Unfortunately as you can read here: [LoRa Library API](https://github.com/sandeepmistry/arduino-LoRa/blob/master/API.md)
Spreading Factor lower than 7 requires an implicit header mode. You can start it by:
`LoRa.beginPacket(implicitHeader);`

But then TTGO (RX) starts to loose about half of packets, making data transfer actually worse than with Sprading Factor = 7.
Also the BAND 433E6 is the best one && LoRa with Arduino needs around 1A power supply to provide the best results.

I didn't change anything in RX, there's not much to tinker around. It just mustn't clear the display very often - it is so slow,
that TTGO misses all packets during this proccess. What's important about TTGO is that its OLED run on SPI, pinout is
pretty weird and writing code for OLED Screen from scratch can be quite hard. I strongly suggest using code that is in this repo.

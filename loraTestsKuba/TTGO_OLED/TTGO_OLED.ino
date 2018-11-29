/*================================================================*/
/* Plastic Monkeys CanSat 2018
/*================================================================*/

#include <U8x8lib.h>
#include <LoRa.h>

/*================================================================*/
/* Some global things
/*================================================================*/

String receivedText;
String receivedRssi;

#define SS      18 //some pins for LoRa
#define RST     14
#define DI0     26
#define BAND    433E6 //Our radio Band

int packetNum = 0; //packets Counter
int first = 0; //ID of first packet
bool startReading = 0; //important to distinguish first reading with others
unsigned long firstReadingTime = 0; //when we received the first reading - necessary to calculate data speed

// the OLED used
U8X8_SSD1306_128X64_NONAME_SW_I2C u8x8(/* clock=*/ 15, /* data=*/ 4, /* reset=*/ 16);


/*================================================================*/
/* Simple function to display a String on our OLED
/*================================================================*/

void printStringOled(String a, int x, int y){
  char temp[64];
  a.toCharArray(temp, 64);
  u8x8.drawString(x, y, temp);
}

/*================================================================*/
/* Setup
/*================================================================*/

void setup() {
  SPI.begin(5, 19, 27, 18); //necessary for OLED
  LoRa.setPins(SS, RST, DI0); //set up a LoRa

  Serial.begin(9600); //start comunicating with a computer
  delay(1000);

  u8x8.begin(); //start Displaying stuff
  u8x8.setFont(u8x8_font_chroma48medium8_r); //set a nice font

  Serial.println("LoRa Receiver");
  u8x8.drawString(0, 1, "LoRa Receiver"); //print some intro stuff

  if (!LoRa.begin(BAND)) {
    Serial.println("Starting LoRa failed!");
    u8x8.drawString(0, 1, "Starting LoRa failed!");
    while (1);
  }
}

/*================================================================*/
/* Loop
/*================================================================*/

void loop() {
  u8x8.drawString(0, 3, "o"); //this is a basic indicator - each time TTGO receives a packet it changes to "x"

  // try to parse packet
  int packetSize = LoRa.parsePacket();
  bool correctPacket = 0; //to check if we received a correct packet
  if (packetSize) { //if we received a correct packet
    while (LoRa.available()) {
      correctPacket = 1;
      u8x8.drawString(0, 3, "x");
      String receivedText =""; //our received text
      String num = ""; // just to obtain our packet ID
      
      for (int i = 0; i < packetSize; i++) {
        char letter = (char) LoRa.read();
        receivedText += letter;
        if(letter - 48 < 10) //if the current char is a number
          num += letter;
      }
      
      int numInt = num.toInt(); //convert obtained packet ID to int
      Serial.print(receivedText); //print our received text
      
      if(startReading == 0){ //some stuff that happens only once - set number of first packet and time when we got it. Necessary for calculating a percentage of received packets.
        startReading = 1;
        first = numInt;
        firstReadingTime = millis()-1; //-1 so we dont divide by 0 during first reading, when calculating data speed
      }
      double percent = ((double)((packetNum))/(numInt-first))*100; //calculate percentage of received packets
      double dataSpeed = (double)(((double)packetNum*1000)/(millis()-firstReadingTime)); //calculate speed of received packets/s
      String info = String(percent) + "% " + String(dataSpeed) + "/s"; //String with all needed data
   
      Serial.println(" -- " + info); //print it to a computer
      printStringOled(info,0,4); //print it to a OLED
    }
    if(correctPacket)
      packetNum++; //Increase number of received packets

    String sRSSI = String(LoRa.packetRssi()); // obtain RSSI of packet
    Serial.println(" with RSSI " + sRSSI); //print it to a computer
    printStringOled(sRSSI,0,5); //print it to a OLED
  }
}

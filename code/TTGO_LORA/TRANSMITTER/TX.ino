#include <LoRa.h> 

#define BAND 433E6
#define SERIAL_RATE 9600

class LED{
  private:
    int myPin;
  public:
    LED(int pin){ 
      pinMode(pin,OUTPUT); 
      myPin = pin;
    }
    void on(){
      digitalWrite(myPin,1);
    }
    void off(){
      digitalWrite(myPin,0);
    }
};

int counter = 0;
int delayTime = 100;
LED led = LED(13);

void setup() {
  Serial.begin(SERIAL_RATE);
  Serial.println("Hello Arduino Lora Sender");
  if (!LoRa.begin(BAND)){
    Serial.println("LoRa Initialization failed:");  
    while(1);
  }
  LoRa.setSpreadingFactor(7);
  LoRa.setTxPower(20);
  Serial.println("LoRa initialization successful");
}

void loop() {
  led.on();
  Serial.print("Sending packet: ");
  Serial.println(counter);

  LoRa.beginPacket();
  LoRa.print(counter);
  LoRa.print(" abababababababababababababababababababababababababababababab");
  LoRa.endPacket();
  counter++;
  
  delay(delayTime/2);
  led.off();
  delay(delayTime/2);
}

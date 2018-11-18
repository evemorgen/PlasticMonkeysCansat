#include "Wire.h"
#include "SSD1306.h"

SSD1306 display(0x3c, 4, 15);


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("hello");

  pinMode(16, OUTPUT);
  digitalWrite(16, LOW);
  delay(50);
  digitalWrite(16, HIGH);


  display.init();
  display.drawString(0, 0, "HelloWorld");
  display.display();
}
void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(millis());
  Serial.println(digitalRead(23));
  display.clear();
  display.drawString(0, 0, "HelloWorld");
  display.drawString(0, 20, "Millis:");
  display.drawString(30, 20, String(millis()));
  display.drawString(0, 40, "Pin 23:");
  display.drawString(40, 40, String(digitalRead(23)));
  display.display();
  delay(200);
}

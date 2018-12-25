const int analogInPin = A3;

// Number of samples to average the reading over
const int avgSamples = 50;
int sensorValue = 0;
long long integral = 0;

float sensitivity = 2.3;
float Vref = 2447; // Output voltage with no current

void setup() {
  Serial.begin(9600);
}

void loop() {
  // read the analog in value:
  for (int i = 0; i < avgSamples; i++)
  {
    sensorValue += analogRead(analogInPin);

    // wait 2 milliseconds before the next loop
    // for the analog-to-digital converter to settle
    // after the last reading:
    delay(2);

  }

  sensorValue = sensorValue / avgSamples;

  // The on-board ADC is 10-bits -> 2^10 = 1024 -> 5V / 1024 ~= 4.88mV
  // The voltage is in millivolts
  float voltage = 4.88 * sensorValue;

  // This will calculate the actual current (in mA)
  // Using the Vref and sensitivity settings you configure
  float current = (voltage - Vref) * sensitivity;
  Serial.print(current);
  //integral += current*avgSamples*2/1000;
  //Serial.print(" ");
  //Serial.println((int)integral);
  sensorValue = 0;
}

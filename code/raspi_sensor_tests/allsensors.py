import sys
import smbus2
import bme280
from time import sleep
from w1thermsensor import W1ThermSensor

i2c = smbus2.SMBus(1)

ds18b20 = W1ThermSensor()
BME280_ADDR = 0x76
BME280_ADDR_IMU = 0x77

print (sys.argv)

while True:
	sleep(0.1)
	if not "-bme280" in sys.argv:
		bme280_data = bme280.sample(i2c, BME280_ADDR)
		print("BME280 Temp: {0:.1f}".format(bme280_data.temperature))
	
	if not "-bme280imu" in sys.argv:
		bme280_data_IMU = bme280.sample(i2c, BME280_ADDR_IMU)
		print("BME280-IMU Temp: {0:.1f}".format(bme280_data_IMU.temperature))
		print("BME280-IMU Pressure: {0:.1f}".format(bme280_data_IMU.pressure))
	
	if not "-ds18b20" in sys.argv:
		ds18b20_temp = ds18b20.get_temperature()
		print("DS18B20 Temp: {0:.1f}".format(ds18b20_temp))
		print("BME280 Pressure: {0:.1f}".format(bme280_data.pressure))
	
	if not "inf" in sys.argv:
		break

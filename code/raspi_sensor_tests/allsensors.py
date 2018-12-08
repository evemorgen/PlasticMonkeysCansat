import sys
import smbus2
import bme280
from time import sleep
from w1thermsensor import W1ThermSensor

i2c = smbus2.SMBus(1)

ds18b20 = W1ThermSensor()
ds18b20_temp = ds18b20.get_temperature()

BME280_ADDR = 0x76
bme280_data = bme280.sample(i2c, BME280_ADDR)

BME280_ADDR_IMU = 0x77
bme280_data_IMU = bme280.sample(i2c, BME280_ADDR_IMU)


def print_data():
	print("DS18B20 Temp: {0:.1f}".format(ds18b20_temp))
	print("BME280 Temp: {0:.1f}".format(bme280_data.temperature))
	print("BME280 Pressure: {0:.1f}".format(bme280_data.pressure))
	print("BME280-IMU Temp: {0:.1f}".format(bme280_data_IMU.temperature))
	print("BME280-IMU Pressure: {0:.1f}".format(bme280_data_IMU.pressure))

print_data()

if len(sys.argv) > 1 and sys.argv[1] == "inf":
	while True:
		sleep(0.1)
		bme280_data = bme280.sample(i2c, BME280_ADDR)
		bme280_data_IMU = bme280.sample(i2c, BME280_ADDR_IMU)
		# ds18b20_temp = ds18b20.get_temperature()
		print_data()

import smbus2
import bme280
from time import sleep

i2c = smbus2.SMBus(1)
# calibration_params = bme280.load_calibration_params(i2c, 0x76)

while True:
	data = bme280.sample(i2c, 0x76)
	print("Pressure: {p:.1f}\nTemp: {t:.1f}\nTime: {ti}\n".format(p=data.pressure, t=data.temperature, ti=data.timestamp))
	sleep(1)

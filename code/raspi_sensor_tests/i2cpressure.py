import smbus2
import bme280
from time import sleep

i2c = smbus2.SMBus(1)
# calibration_params = bme280.load_calibration_params(i2c, 0x76)


data = bme280.sample(i2c, 0x76)
print("GY-BMP280 Pressure: {p:.1f}\nGY-BMP280 Temp: {t:.1f}\n".format(p=data.pressure, t=data.temperature))


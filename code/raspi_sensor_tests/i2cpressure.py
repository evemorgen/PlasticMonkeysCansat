import smbus2
import bme280
from time import sleep

address = 0x77
i2c = smbus2.SMBus(1)
# calibration_params = bme280.load_calibration_params(i2c, address)

data = bme280.sample(i2c, address)
print("BMP280 Pressure: {0:.1f}".format(data.pressure))
print("BMP280 Temp: {0:.1f}".format(data.temperature))

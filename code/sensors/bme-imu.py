import smbus2
import bme280
from time import sleep

address = 0x77
i2c = smbus2.SMBus(1)
# calibration_params = bme280.load_calibration_params(i2c, address)

while True:
    data = bme280.sample(i2c, address)
    pres_int = round((data.pressure-600)/4) # delta_p=4hPa range=(600, 1108)hPa
    temp_int = round((data.temperature+30)*2) # delta_t = 0.5*C range=(-30, 33)*C
    t = open("/home/pi/sensor-logs/bme-imu-temp", "a")
    t.write(str(temp_int) + "\n")
    t.close()
    p = open("/home/pi/sensor-logs/bme-imu-pres", "a")
    p.write(str(pres_int) + "\n")
    p.close()
    sleep(0.2)

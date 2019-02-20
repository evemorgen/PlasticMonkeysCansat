import bme680
from time import sleep

bme = bme680.BME680(bme680.I2C_ADDR_PRIMARY)

while True:
    if bme.get_sensor_data():
        pres_int = round((bme.data.pressure-600)/4) # delta_p=4hPa range=(600, 1108)hPa
        temp_int = round((bme.data.temperature+30)*2) # delta_t = 0.5*C range=(-30, 33)*C
        p = open("/home/pi/sensor-logs/bme-ext-pres", "a")
        p.write(str(pres_int)+'\n')
        t = open("/home/pi/sensor-logs/bme-ext-temp", "a")
        t.write(str(temp_int)+'\n')
        sleep(0.2)

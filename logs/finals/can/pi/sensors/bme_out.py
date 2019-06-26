import smbus2
import bme280
from time import sleep

address = 0x76
i2c = smbus2.SMBus(1)
log_path_temp = "/home/pi/sensor_logs/out_temp.txt"
log_path_pres = "/home/pi/sensor_logs/out_pres.txt"

while True:
    data = bme280.sample(i2c, address)
    t = str(round((data.temperature+25)*2)) # range(-25, 38) delta=0.5
    p = str(round((data.pressure-450)/5)) # range(450, 1090) delta=5
    #print("BMP280 Pressure: {0:.1f}".format(p))
    #print("BMP280 Temp: {0:.1f}".format(t))
    t = "out_temp: " + t
    t += "-"*(24-len(t))
    p = "out_pres: " + p
    p += "-"*(24-len(p))
    tf = open(log_path_temp, "a")
    tf.write(t)
    tf.close()
    pf = open(log_path_pres, "a")
    pf.write(p)
    pf.close()
    sleep(0.8)

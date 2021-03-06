import sys
import smbus2
import bme280
import configparser
from time import sleep, time

config_file = sys.argv[1]
config = configparser.ConfigParser()
config.read(config_file)

address = int(config['SETTINGS']['address'], 16)
log_path_temp = config['PATHS']['temperature_log']
log_path_pres = config['PATHS']['pressure_log']
sleep_time = float(config['SETTINGS']['sleep_time'])

i2c = smbus2.SMBus(1)

while True:
    try:
        data = bme280.sample(i2c, address)
        t = int(round((data.temperature+25)*10)) # range(-25, 38) delta=0.1
        p = round((data.pressure-450)*10) # range(450, 1090) delta=0.1
        timestamp = round(time())
        #print("BMP280 Pressure: {0}".format(p))
        #print("BMP280 Temp: {0}".format(t))
        output_t = ('{} {}\n').format(timestamp,t)
        output_p = ('{} {}\n').format(timestamp,p)
        tf = open(log_path_temp, "a")
        tf.write(output_t)
        tf.close()
        pf = open(log_path_pres, "a")
        pf.write(output_p)
        pf.close()
        sleep(sleep_time)
    except Exception:
        sleep(sleep_time)

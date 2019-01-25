import sys
import smbus2
import bme280
import serial
import pynmea2
from time import time, sleep
from w1thermsensor import W1ThermSensor

i2c = smbus2.SMBus(1)

ds18b20 = W1ThermSensor()
BME280_ADDR = 0x76
BME280_ADDR_IMU = 0x77

gps_port_path = "/dev/serial0"
gps_serial_port = serial.Serial(gps_port_path, baudrate = 9600, timeout = 0.5)

a = time()

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
    
    if not "-gps" in sys.argv:
        line = gps_serial_port.readline()
        while line.find("GGA") < 0: 
            line = gps_serial_port.readline()
        
        msg = pynmea2.parse(line)
        print("Timestamp: {0}".format(msg.timestamp))
        print("Lat: {0:.5f} {1}".format(msg.latitude, msg.lat_dir))
        print("Lon: {0:.5f} {1}".format(msg.longitude, msg.lon_dir))
        print("Alt: {0} {1}".format(msg.altitude, msg.altitude_units))
        print("Satelites used: {0}".format(msg.num_sats))
    
    if not "-time" in sys.argv:
        print("Time since last read: {0:.3f}".format(time() - a))
        a = time()
    
    if not "inf" in sys.argv:
        break
    
    print("-------------------------------")

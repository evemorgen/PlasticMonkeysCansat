import serial
import pynmea2
from time import sleep, time

port_path = "/dev/serial0"
serialPort = serial.Serial(port_path, baudrate = 9600, timeout = 0.5)

a = time()

def parseGPS(line):
	if line.find("GGA") > 0:
		msg = pynmea2.parse(line)
		print("Timestamp: {0}".format(msg.timestamp))
		print("Lat: {0} {1}".format(msg.lat, msg.lat_dir))
		print("Lon: {0} {1}".format(msg.lon, msg.lon_dir))
		print("Alt: {0} {1}".format(msg.altitude, msg.altitude_units))
		print("Satelites used: {0}".format(msg.num_sats))
		print("Time since last read: {0:.3f}".format(time() - a))

while True:
	line = serialPort.readline()
	parseGPS(line)
	a = time()

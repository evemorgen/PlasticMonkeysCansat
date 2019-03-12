import serial
import pynmea2
from time import sleep, time

port_path = "/dev/serial0"
serialPort = serial.Serial(port_path, baudrate = 9600, timeout = 0.5)

log_path = "/home/pi/sensor_logs/gps.txt"

def parseGPS(line):
    if line.find("GGA") > 0:
        msg = pynmea2.parse(line)
        t = (msg.timestamp.hour * 60 + msg.timestamp.minute) * 60 + msg.timestamp.second
        lat = round((msg.latitude+90)*100000)
        lon = round((msg.longitude+180)*100000)
        alt = round(msg.altitude)
        # print("Timestamp: {0}".format(t))
        # print("Lat: {0}".format(lat))
        # print("Lon: {0}".format(lon))
        # print("Alt: {0}".format(alt))
        output = str(t) + " " + str(lat) + " " + str(lon) + " " + str(alt) + "\n"
        f = open(log_path, "a")
        f.write(output)
        f.close()


while True:
    line = serialPort.readline().decode('utf-8')
    parseGPS(line)

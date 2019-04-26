import serial
import pynmea2
import configparser
from time import sleep, time

config_file = sys.argv[1]
config = configparser.ConfigParser()
config.read(config_file)

port_path = config['SETTINGS']['uart_port_path']
uart_baudrate = int(config['SETTINGS']['uart_baudrate'])
uart_timeout = float(config['SETTINGS']['uart_timeout'])
sleep_time = float(config['SETTINGS']['sleep_time'])

latitude_log = config['PATHS']['gps_latitude_log']
longitude_log = config['PATHS']['gps_longtitude_log']
altitude_log = config['PATHS']['gps_altitude_log']
timestamp_log = config['PATHS']['gps_timestamp_log']

serialPort = serial.Serial(port_path, baudrate = uart_baudrate, timeout = uart_timeout)

def parseGPS(line):
    if line.find("GGA") > 0:
        msg = pynmea2.parse(line)
        tim = (msg.timestamp.hour * 60 + msg.timestamp.minute) * 60 + msg.timestamp.second
        lat = round((msg.latitude+90)*100000)
        lon = round((msg.longitude+180)*100000)
        alt = round(msg.altitude)
        unix_timestamp = round(time())

        file_dict = {
            'latitude': [latitude_log, lat],
            'longtitude': [longtitude_log, lon],
            'altitude': [altitude_log, alt],
            'timestamp': [timestamp_log, tim]
        }

        for type in file_dict:
            open_file = open(file_dict[type][0], "a")
            open_file.write(('{} {}\n').format(unix_timestamp,file_dict[type][1]))
            open_file.close()


while True:
    try:
        line = serialPort.readline().decode('utf-8')
        parseGPS(line)
        sleep(sleep_time)
    except Exception:
        sleep(sleep_time)

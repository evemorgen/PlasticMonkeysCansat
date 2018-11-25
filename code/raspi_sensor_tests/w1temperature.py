import os
from glob import glob
from time import sleep

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_raw():
	f = open(device_file)
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_raw()
	
	value_pos = lines[1].find('t=')
	if value_pos != -1:
		temp_string = lines[1][value_pos+2:]
		temp = float(temp_string)/1000.0
		return temp

print("DS18B20 Temp: {t:.1f}".format(t=read_temp()))

import os
import sys
from time import sleep

dir = "/home/pi/Desktop/PlasticMonkeysCanSat/code/raspi_sensor_tests/"

def run_scripts():
	os.system("python "+ dir + "i2cpressure.py")
	os.system("python "+ dir + "w1temperature.py")

run_scripts()

if len(sys.argv) > 1:
	if sys.argv[1] == "inf":
		while True:
			sleep(2)
			run_scripts()

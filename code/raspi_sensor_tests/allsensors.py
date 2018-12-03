import os
import sys
from time import sleep

dir = "/home/pi/Desktop/PlasticMonkeysCanSat/code/raspi_sensor_tests/"

def run_scripts():
	os.system("python "+ dir + "i2cpressure.py")
#	os.system("python "+ dir + "w1temperature.py")

run_scripts()

if len(sys.argv) > 1 and sys.argv[1] == "inf":
	while True:
		sleep(0.1)
		run_scripts()

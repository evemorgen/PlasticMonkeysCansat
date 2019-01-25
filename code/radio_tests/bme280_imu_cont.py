import smbus2
import bme280
from time import sleep

address = 0x77
i2c = smbus2.SMBus(1)

f = open("tx.txt", "w")

while True:
	data = bme280.sample(i2c, address)
	f = open("tx.txt", "w")
	f.write("T: " + str(round(data.temperature, 1)) + "P: ") 
	f.write(str(round(data.pressure, 0)) + "\n")
	f.close()
	sleep(0.5)

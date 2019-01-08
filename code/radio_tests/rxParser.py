import RPi.GPIO as GPIO
from time import sleep

led_pin = 31
buzzer_pin = 29

GPIO.setmode(GPIO.BOARD)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(led_pin, GPIO.OUT)

while True:
	f = open("rx.txt", "r")
	line = f.readline()
	if "L" in line:
		i = line.index("L")
		val = line[i+1]
		if val == "1":
			GPIO.output(led_pin, True)
		elif val == "0":
			GPIO.output(led_pin, False)

	if "B" in line:
		i = line.index("B")
		val = line[i+1]
		if val == "1":
			GPIO.output(buzzer_pin, True)
		elif val == "0":
			GPIO.output(buzzer_pin, False)

	f.close()
	sleep(0.05)

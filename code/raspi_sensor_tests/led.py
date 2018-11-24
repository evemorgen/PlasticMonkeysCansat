import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, False)

while True:
    GPIO.output(11, True)
    sleep(1)
    GPIO.output(11, False)
    sleep(1)

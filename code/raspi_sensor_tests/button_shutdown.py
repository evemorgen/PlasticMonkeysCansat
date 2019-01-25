import os
from time import time
import RPi.GPIO as GPIO


def press(channel):
    shutdown = False
    start_time = time()
    GPIO.output(led_output, True)
    while GPIO.input(channel) == GPIO.HIGH:
        if 10 > time() - start_time > 5:
            GPIO.output(led_output, False)
        if time() - start_time > 10:
            GPIO.output(led_output, True)
            shutdown = True
    GPIO.output(led_output, False)

    if shutdown:
        os.system("shutdown now -h")

GPIO.setmode(GPIO.BOARD)

btn_input = 40
led_output = 37

GPIO.setup(btn_input, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led_output, GPIO.OUT)

GPIO.add_event_detect(btn_input, GPIO.RISING, callback=press)

try:
    while True:
        pass
except:
    GPIO.cleanup()

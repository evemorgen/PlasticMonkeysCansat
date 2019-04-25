import sys
import configparser
import RPi.GPIO as GPIO
import time

config_file = sys.argv[1]
config = configparser.ConfigParser()
config.read(config_file)

led_pin = int(config['SETTINGS']['led_pin'])
delay = float(config['SETTINGS']['delay'])
exception_sleep_time = float(config['SETTINGS']['exception_sleep_time'])

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led_pin,GPIO.OUT)

while True:
    try:
        GPIO.output(led_pin,GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(led_pin,GPIO.LOW)
        time.sleep(delay)
    except Exception as ex:
        print(ex)
        time.sleep(exception_sleep_time)
    finally:
        GPIO.output(led_pin,GPIO.LOW)

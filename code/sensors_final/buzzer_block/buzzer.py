import sys
import RPi.GPIO as GPIO
import configparser
from time import sleep

config_file = sys.argv[1]
config = configparser.ConfigParser()
config.read(config_file)

buzzer_pin= int(config['SETTINGS']['buzzer_pin'])
delay_on = float(config['SETTINGS']['delay_on'])
delay_off = float(config['SETTINGS']['delay_off'])
frequency = int(config['SETTINGS']['frequency'])

GPIO.setmode(GPIO.BOARD)
GPIO.setup(buzzer_pin, GPIO.OUT)

p = GPIO.PWM(buzzer_pin, frequency)

while True:
    try:
        p.start(50)
        sleep(delay_on)
        p.stop()
        sleep(delay_off)
    except Exception as ex:
        print(ex)
        sleep(0.1)
    finally:
        p.stop()
        GPIO.cleanup()

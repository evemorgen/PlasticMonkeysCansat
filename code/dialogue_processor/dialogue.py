import configparser
import sys
import time
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

config_file = sys.argv[1]
config = configparser.ConfigParser()
config.read(config_file)

left_pin = int(config['SETTINGS']['left_pin'])
center_pin = int(config['SETTINGS']['center_pin'])
right_pin = int(config['SETTINGS']['right_pin'])

oled_buffer = config['PATHS']['oled_buffer']
output_log = config['PATHS']['output_log']

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

GPIO.setup(left_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(center_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(right_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(left_pin,GPIO.RISING,callback=left_pin) # Setup event on pin 10 rising edge
GPIO.add_event_detect(center_pin,GPIO.RISING,callback=center_pin) # Setup event on pin 10 rising edge
GPIO.add_event_detect(right_pin,GPIO.RISING,callback=right_pin) # Setup event on pin 10 rising edge

all = config.items("QUESTIONS")
questions = [second for first,second in all]

question_num = 0

buffer = open(oled_buffer, "w")
try:
    buffer.write(questions[question_num])
except Exception:
    pass

def left_callback(channel):
    print("left button clicked")
    file = open(output_log, "a")
    file.write(('{}:L ').format(question_num))
    file.close()
    question_num = question_num+1;
    buffer = open(oled_buffer, "w")
    try:
        buffer.write(questions[question_num])
    except Exception:
        pass
    while GPIO.input(left_pin) == 1:
        pass


def center_callback(channel):
    print("center button clicked")
    file = open(output_log, "a")
    file.write(('{}:C ').format(question_num))
    file.close()
    question_num = question_num+1;
    buffer = open(oled_buffer, "w")
    try:
        buffer.write(questions[question_num])
    except Exception:
        pass
    while GPIO.input(center_pin) == 1:
        pass

def right_callback(channel):
    print("right button clicked")
    file = open(output_log, "a")
    file.write(('{}:R ').format(question_num))
    file.close()
    question_num = question_num+1;
    buffer = open(oled_buffer, "w")
    try:
        buffer.write(questions[question_num])
    except Exception:
        pass
    while GPIO.input(right_pin) == 1:
        pass

while True:
    pass

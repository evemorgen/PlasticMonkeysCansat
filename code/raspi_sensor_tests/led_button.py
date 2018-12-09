import RPi.GPIO as GPIO

led_pin = 33
button_pin = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led_pin, GPIO.OUT)

while True:
    if GPIO.input(button_pin) == GPIO.HIGH:
        GPIO.output(led_pin, True)
    else:
        GPIO.output(led_pin, False)

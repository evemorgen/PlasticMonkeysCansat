import RPi.GPIO as GPIO

led_pin = 29
button_pin = 40
buzzer_pin = 31 

GPIO.setmode(GPIO.BOARD)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)

while True:
	if GPIO.input(button_pin) == GPIO.HIGH:
		GPIO.output(led_pin, True)
		GPIO.output(buzzer_pin, True)
	else:
		GPIO.output(led_pin, False)
		GPIO.output(buzzer_pin, False)

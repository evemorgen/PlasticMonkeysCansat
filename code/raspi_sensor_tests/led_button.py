import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(11, GPIO.OUT)

while True:
	if GPIO.input(40) == GPIO.HIGH:
		GPIO.output(11, True)
	else:
		GPIO.output(11, False)

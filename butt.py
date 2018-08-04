import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

if (GPIO.input(4)==1):
	execfile('enterrback.py')
else
	print "Please press calling bell"



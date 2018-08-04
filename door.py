import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(37, GPIO.OUT)

p = GPIO.PWM(37, 50)


p.start(7.5)

try:
	
	p.ChangeDutyCycle(7.5)#turn towards 90
	
	time.sleep(10)

	p.ChangeDutyCycle(2.5)#turn towards 0
	time.sleep(2)
	GPIO.cleanup()

	
	#p.ChangeDutyCycle(12.5)
	#time.sleep(1)
except KeyboardInterrupt:
	p.stop()
	GPIO.cleanup()

		

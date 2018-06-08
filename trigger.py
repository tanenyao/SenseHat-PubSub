import RPi.GPIO as GPIO
from sensor import readAdc, SPICLK, SPIMOSI, SPIMISO, SPICS

GPIO.setmode(GPIO.BCM)

switch = 17
ledOne = 27
ledTwo = 22

GPIO.setup(switch, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(ledOne, GPIO.OUT)
GPIO.setup(ledTwo, GPIO.OUT)

battery = 0

def readVolts():
	s, reps = 0, 1024
	for x in range(reps):
		k = readAdc(battery, SPICLK, SPIMOSI, SPIMISO, SPICS)
		s += k
	s = s/reps/1.0
	volts = s*(3.3/1024)*3.05
	return volts

def lowVoltage(cutoff):
	v = readVolts()
	if v < cutoff:
		return True
	else:
		return False

def turnOff():
	if GPIO.input(switch) == False:
		return True
	else:
		return False

def ledOn(led):
	GPIO.output(led, True)

def ledOff(led):
	GPIO.output(led, False)


import RPi.GPIO as GPIO
import math
from sense_hat import SenseHat

GPIO.setmode(GPIO.BCM)

mic = 1
SPICLK = 0
SPIMISO = 5
SPIMOSI = 6
SPICS = 13

GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICS, GPIO.OUT)

sense = SenseHat()

def readAdc(adcnum, clockpin, mosipin, misopin, cspin):
	if ((adcnum > 7) or ( adcnum < 0)):
		return -1
	GPIO.output(cspin, True)
	GPIO.output(clockpin, False)
	GPIO.output(cspin, False)

	commandout = adcnum
	commandout |= 0x18
	commandout <<= 3
	for i in range(5):
		if (commandout & 0x80):
			GPIO.output(mosipin, True)
		else:
			GPIO.output(mosipin, False)
		commandout <<= 1
		GPIO.output(clockpin, True)
		GPIO.output(clockpin, False)

	adcout = 0
	for i in range(12):
		GPIO.output(clockpin, True)
		GPIO.output(clockpin, False)
		adcout <<= 1
		if (GPIO.input(misopin)):
			adcout |= 0x1

	adcout >>= 1
	return adcout

def readSensehat():
	t = sense.get_temperature()
	h = sense.get_humidity()
	p = sense.get_pressure()
	a = sense.get_accelerometer_raw()
	m = sense.get_compass_raw()
	g = sense.get_gyroscope_raw()
	return t,h,p,a,m,g

def readMic():
	ref = 1024/2
	sample = 1024
	s, amp = 0,0
	for x in range(sample):
		k = readAdc(mic, SPICLK, SPIMOSI, SPIMISO, SPICS)
		amp = abs(k-ref)
		s += amp*amp
	s /= sample
	s = math.sqrt(s)
	db = 20 * math.log10(s/ref)
	return db

def data():
	return readSensehat() + (readMic(),)

import paho.mqtt.publish as publish, os, time

from sensor import data
from trigger import *
from pub import createTopic, createPayload, createPubMessage
from timelog import startRec, endRec
from clock import ntpClock

#ntpClock()

startRec()

#broker = "st-mct-vm25"
broker = "10.218.68.90"

time.sleep(5)
try:
	while True:
		if (shutdownVolts(6.8) == True):
			endRec()

			ledOn(ledTwo)
			ledOff(ledOne)

			time.sleep(2)
			GPIO.cleanup()
			#os.system("sudo shutdown -h now")
			break

		ledOn(ledOne)
		ledOff(ledTwo)

		topic = createTopic()
		payload = createPayload(data())
		pubMsg = createPubMessage(topic, payload)

		publish.multiple(pubMsg, broker)
		print("Publish Success...")

except KeyboardInterrupt:
	GPIO.cleanup()
	print("exit")

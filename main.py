import paho.mqtt.publish as publish
import os
import time
from datetime import datetime
from sensor import data
from trigger import *
from pub import createTopic, createPayload, createPubMessage

#ntpClock()
#broker = "st-mct-vm25"
broker = "10.218.68.90"

def ntpClock():
	os.system("sudo service ntp stop")
	os.system("sudo ntpdate 172.20.114.1")
	os.system("sudo service ntp start")

# file and functions to record time
def rmfile(filename):
	try:
		os.remove(filename)
	except OSError as e:
		if e.errno != errno.ENOENT:
			raise

def writeLog(logline):
	logfile = open('logs.txt', 'a')
	logfile.write(logline + '\n')
	logfile.close()

rmfile('logs.txt')

item = "Battery log data"
logfile = open('logs.txt', 'w')
recTime = datetime.today().strftime("%Y-%m-%d %H:%M:%S")[:-3]
logfile.write(item + '\n' + "Starting at" + recTime + '\n')
logfile.close()
# end

time.sleep(10)
try:
	while True:
		# time recording
		#recTime = datetime.today().strftime("%Y-%m-%d %H:%M:%S")[:-3]
		#volts = str(readVolts())
		#logline = '%s, %s' % (recTime, volts)
		#writeLog(logline)
		# end

		if (shutdownVolts(6.8) == True):
			# time recording
			recTime = datetime.today().strftime("%Y-%m-%d %H:%M:%S")[:-3]
			logline = "Stopping due to low V at" + recTime
			writeLog(logline)
			# end

			ledOn(ledTwo)
			ledOff(ledOne)
			time.sleep(2)
			break
			#GPIO.cleanup()
			#os.system("sudo shutdown -h now")

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

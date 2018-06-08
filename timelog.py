import os, errno
from datetime import datetime
from trigger import turnOff

f = 'log.txt'

def recTime():
	s = datetime.today().strftime("%Y-%m-%d %H:%M:%S")[:-3]
	return s

def rmFile():
	try:
		os.remove(f)
	except OSError as e:
		if e.errno != errno.ENOENT:
			raise

def startRec():
	#rmFile()

	logfile = open(f, 'a')
	logfile.write("Starting at " + recTime() + '\n')
	logfile.close()

def endRec():
	if turnOff():
		s = "off button pressed"
	else:
		s = "low voltage"

	logfile = open(f, 'a')
	logfile.write("Stopping due to " + s + " at " + recTime() + '\n\n')
	logfile.close()

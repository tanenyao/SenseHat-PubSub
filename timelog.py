import os, errno
from datetime import datetime

f = 'log.txt'

def recTime():
	s = datetime.today().strftime("%Y-%m-%d %H:%M:%S")[:-3]
	return s


def startRec():
	try:
		os.remove(f)

	except OSError as e:
		if e.errno != errno.ENOENT:
			raise

	title = "Battery Log"
	logfile = open(f, 'w')
	logfile.write(title + '\n\n' + "Starting at " + recTime() + '\n')
	logfile.close()

def endRec():
	logfile = open(f, 'a')
	logfile.write("Stopping due to low V at " + recTime())
	logfile.close()

import os

def ntpClock():
	os.system("sudo service ntp stop")
	os.system("sudo ntpdate 172.20.114.1")
	os.system("sudo service ntp start")

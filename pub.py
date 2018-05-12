import json
from collections import OrderedDict
from datetime import datetime

sensors = ['Temperature', 'Humidity', 'Pressure', 'Accelerometer', 'Magnetometer', 'Gyroscope', 'Sound']

def createTopic():
	topics = []
	for x in sensors:
		topics.append("Sensors/RaspberryPi01/SenseHat01/" + x)
	return topics

def idType(tup):
	intOrDict = []
	for x in tup:
		intOrDict.append(type(x))
	return intOrDict

def timestamp():
	now = datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
	string = '"Timestamp": "%s"' % now
	return string

def createPayload(tup):
	if len(tup) != len(sensors):
		return -1

	payload = []
	time = timestamp()
	for i in range(len(tup)):
		if isinstance(tup[i], float):
			payload.append(json.loads('{%s, "%s_Actual_Value": "%.2f"}' % (time, sensors[i], tup[i])))

		if isinstance(tup[i], dict):
			new_tup = sorted(tup[i].items())
			string = '{' + time + ', '
			for k,v in new_tup:
				string += '"%s_Actual_%s_Value" : "%.2f", ' % (sensors[i], k, v)
			string = string[:-2]
			string += '}'
			payload.append(json.loads(string, object_pairs_hook=OrderedDict))
	return payload

def createPubMessage(topic, payload):
	qos = 0
	ret = False
	l = []
	for i, j in enumerate(payload):
		tup = ()
		tup += (topic[i],) + (json.dumps(j),) + (qos,) + (ret,)
		l.append(tup)
	return l

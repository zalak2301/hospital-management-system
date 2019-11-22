# hospital-management-system
this is my first repository on Github
import os
import datetime
import time
import firebase_admin
import serial
from google.cloud import firestore
from firebase_admin import credentials
from firebase_admin import firestore


x = datetime.datetime.now()
print(x)
def read_rfid():
	ser=serial.Serial("/dev/ttyUSB2")
	ser.baudrate = 9600
	data = ser.read(12)
	ser.close()
	return data
cred = credentials.Certificate("/rfid/rfid-receive-firebase-adminsdk-ysyuj-6ac5cdc24c.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

while True:
	print(" ")
	print("Place your card:")
	detection = read_rfid()
	#print (detection)
	print("Collecting your Data")
	time.sleep(1)
	docs= db.collection(u'Patients').where(u'RFID', u'==',str(detection)).get()
	for detection in docs:
		print("Yeah We Found your data")
		print(" ")
		time.sleep(1)		
		print(u'Welcome:{}'.format(detection.id))
		time.sleep(2)		
		var = db.collection(u'Patients').document(detection.id).get()
		print("Your Registered E-Mail is: ",var.get(u'Email'))
		print("Your Registered Mobile Number is: ",var.get(u'Mobile'))
		time.sleep(2)
		name=docs.format(detection.id)
		print(name)
		os.system("mosquitto_pub -h 192.168.1.76 -t welcome -m 'name'")
	trt = var.get(u'Treatment')
	print("Last time you were here for: ",trt)
	print(" ")
	h=input("Would you like to change the treatment?[y/n]")
	abc = db.collection(u'Doctors').where(u'Specification',u'==',str(trt)).get()	
	if h == 'n':
		for trt in abc:	
			print("")		
			print(u'Doctor available: {}'.format(trt.id))
			xy=db.collection(u'Doctors').document(trt.id).get()
			print("The Appointment Time for the doctor is: ",xy.get(u'Appointment_Time'))
			#print("The Cabin of the doctor is on: ",xy.get(u'Cabin'))	
			time.sleep(1)
	else:
		treatment=input("Which treatment do you want?")
		c = db.collection(u'Doctors').where(u'Specification',u'==',str(treatment)).get()		
		for treatment in c:
			print("")		
			print(u'Doctor available: {}'.format(treatment.id))
			s=db.collection(u'Doctors').document(treatment.id).get()
			print("The Appointment Time for the doctor is: ",s.get(u'Appointment_Time'))
			#print("The Cabin of the doctor is on: ",xy.get(u'Cabin'))	
			time.sleep(1)
			#print("With which Dr. do you want to continue?")
			
		

		

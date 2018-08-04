
import cv2
import random
import config
import face
import httplib, urllib
import time
import RPi.GPIO as GPIO

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart 




if __name__ == '__main__':
	# Load training data into model
	print 'Loading training data...'
	model = cv2.createEigenFaceRecognizer()
	model.load(config.TRAINING_FILE)
	print 'Training data loaded!'
	# Initialize camera
	camera = config.get_camera()
	
	print 'Detecting Face'
	print 'Press Ctrl-C to quit.'
	while True:
		
		result=None
		while(result==None):
			image = camera.read()
				# Convert image to grayscale.
			image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
				# Get coordinates of single face in captured image.
			result = face.detect_single(image)
		if result is None:
			print 'Could not detect single face!  Check the image in capture.pgm' \
		  	' to see what was captured and try again with only one face visible.'
			continue
		x, y, w, h = result
		# Crop and resize image to face.
		crop = face.resize(face.crop(image, x, y, w, h))
		# Test face against model.
		label, confidence = model.predict(crop)
		print 'Predicted {0} face with confidence {1} (lower is more confident).'.format(
			'POSITIVE' if label == config.POSITIVE_LABEL else 'NEGATIVE', 
			confidence)
		print label
		if label == config.POSITIVE_LABEL and confidence < config.POSITIVE_THRESHOLD:
			print 'Recognized face!'
			execfile('led.py') 
			otp=random.randint(1000,10000)
			print otp
			


			def SendMail(ImgFileName):
				img_data = open(ImgFileName, 'rb').read()
				msg = MIMEMultipart()
				msg['Subject'] = 'subject'
				msg['From'] = 'e@mail.cc'
				msg['To'] = 'e@mail.cc'
				s1=str(otp)
				text = MIMEText(s1)
				msg.attach(text)
				image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
				msg.attach(image)

				s = smtplib.SMTP('smtp.gmail.com', 587)
				s.ehlo()
				s.starttls()
				s.ehlo()
				s.login('milindagarwal95@gmail.com', 'Imssgoku8*')
				s.sendmail('milindagarwal95@gmail.com' , 'milindfreak@gmail.com',msg.as_string())
				s.quit()
			filename='IMG_' + '.png'
			print 'Taking Your Image!!' 
			os.system('raspistill -o ' + filename)
			print 'Sending mail.....'
			SendMail(filename)
			print 'Mail Sent'
			print 'enter the otp'
			ue=raw_input()
			if(int(ue)==otp):
				
				print 'You Can Enter'
				time.sleep(1)
				execfile('door.py')
							
			else:
				print 'You are not who you claim  to be.'

			#thingspeak
			
			try:
				params = urllib.urlencode({'field1': int(otp),'key':'0G1662WMZB4MALUQ'})
				headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept":"text/plain"}
				conn = httplib.HTTPConnection("api.thingspeak.com:80")
				conn.request("POST", "/update", params, headers)
				response = conn.getresponse()
				conn.close()
			except:
				print "exception"
			


			
			break
		else:
			print 'Did not recognize face!'

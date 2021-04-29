from imutils.video import VideoStream
import face_recognition
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import os 
from socket import * 

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=True,
	help = "path to where the face cascade resides")
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
args = vars(ap.parse_args())
data = pickle.loads(open(args["encodings"], "rb").read())
detector = cv2.CascadeClassifier(args["cascade"])
vs = VideoStream(src=0).start()
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = None
host = "10.0.0.122" #set to private ip of target machine, i.e., server
port = 13000 
addr = (host, port) 
UDPSock = socket(AF_INET, SOCK_DGRAM)
while True:
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	# Writing to faceRecognitionDemo.mp4
	if writer is None:
		(h, w) = frame.shape[:2]
		writer = cv2.VideoWriter("faceRecognitionDemo.mp4", fourcc, 10,
			(w, h), True)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)
	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
	# boxes = face_recognition.face_locations(rgb, model="hog") # works but too slow
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []
	for encoding in encodings:
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = "Unknown"
		if True in matches:
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1
			name = max(counts, key=counts.get)
			UDPSock.sendto(str.encode(name), addr)
		names.append(name)

	for ((top, right, bottom, left), name) in zip(boxes, names):
		cv2.rectangle(frame, (left, top), (right, bottom),
			(0, 255, 0), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (0, 255, 0), 2)
	cv2.imshow("Frame", frame)
	writer.write(frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
cv2.destroyAllWindows()
vs.stop()
UDPSock.close() 
os._exit(0)

from imutils.video import VideoStream
import argparse
import imutils
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=True,
	help = "path to where the face cascade resides")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory")
args = vars(ap.parse_args()) 
# vars returns the __dict__ value of the object. Now we can access the argument values as such args["cascade"] or args["output"]
detector = cv2.CascadeClassifier(args["cascade"])
vs = VideoStream(src=0).start()
total = 0
while True:
	frame = vs.read()
	orig = frame.copy()
	frame = imutils.resize(frame, width=500)
	# detect faces in gray scale because that is what cv2's haarcascade is trained on
	rects = detector.detectMultiScale(
		cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30))
	for (x, y, w, h) in rects:
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("k"):
		path = os.path.sep.join([args["output"], "{}.png".format(
			str(total).zfill(4))])
		cv2.imwrite(path, orig) # write in BGR format
		total += 1
	elif key == ord("q"):
		break

print("{} images stored".format(total))
cv2.destroyAllWindows()
vs.stop()

from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
	help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())
imagePaths = list(paths.list_images(args["dataset"]))
# imagePaths look like ['dataset/calvin/00022.png', 'dataset/calvin/00027.png', 'dataset/calvin/00012.png', 'dataset/calvin/00006.png' ...]
knownEncodings = []
knownNames = []
for (i, imagePath) in enumerate(imagePaths):
	# extract the person name from the image path
	print("Processing image {}/{}".format(i+1, len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	boxes = face_recognition.face_locations(rgb, model=args["detection_method"])
	encodings = face_recognition.face_encodings(rgb, boxes)
	for encoding in encodings:
		knownEncodings.append(encoding)
		knownNames.append(name)
data = {"encodings": knownEncodings, "names": knownNames}
# data looks like 
#	{'encodings': [array([-8.05334076e-02,  1.16696097e-01,  2.93848608e-02, -7.05346614e-02,
#    -1.31713435e-01, -3.85303888e-03, -1.37290180e-01, -9.73772109e-02,
#     8.18503574e-02, -1.30762324e-01,  2.60778338e-01, -2.51589343e-04, ...,
# 	  3.64202671e-02])], 
#	'names': ['calvin', 'calvin', ...
# 	 'calvin', 'calvin', 'calvin']}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()
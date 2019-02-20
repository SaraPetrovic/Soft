# USAGE
# python neural_network.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# import the necessary packages
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import pyautogui

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

cap = cv2.VideoCapture(0)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) 
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) 
print "HEIGHT " + repr(height) #480
print "WIDTH " + repr(width) #640

while(cap.isOpened()):
	
	ret, frame = cap.read()
	frame = cv2.flip(frame, 1)

	cv2.line(frame,(450,0),(450,640),(255,0,0),5)
	cv2.line(frame,(150,240),(450, 240),(255,0,0),5)
	cv2.line(frame,(150,0),(150,640),(255,0,0),5)

	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
		0.007843, (300, 300), 127.5)

	net.setInput(blob)
	detections = net.forward()

	max_area = 0
	counture = 22
	startX = 0
	startY = 0
	endX = 0
	endY = 0

	for i in  np.arange(0, detections.shape[2]):
		confidence = detections[0, 0, i, 2]
		idx = int(detections[0, 0, i, 1])

		if confidence > args["confidence"] and CLASSES[idx] == 'bottle':
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			area = (endX - startX) * (endY - startY)
			if area > max_area:
				max_area = area
				counture = idx

	if counture != 22:
		label = "{}: {:.2f}%".format(CLASSES[counture], confidence * 100)
		cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[counture], 2)
		y = startY - 15 if startY - 15 > 15 else startY + 15
		cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[counture], 2)

		centroid_x = (startX + endX) / 2
		centroid_y = (startY + endY) / 2
		cv2.circle(frame, (centroid_x, centroid_y), 2, (0,0,255), 2)

		# down-up move
		if centroid_x >= 200 and centroid_x <= 400:
			if centroid_y >= 0 and centroid_y <= 240:
				print "up"
    			pyautogui.press('up')
			if centroid_y >= 240 and centroid_y <=480:
				print "down"
    			pyautogui.press('down')

		# left-right move
		if centroid_y >= 0 and centroid_y <= 480:
			if centroid_x >= 0 and centroid_x <= 150:
				print "left"
        		pyautogui.press('left')
    		if centroid_x >= 450:
				print "right"
				pyautogui.press('right')


	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

cv2.destroyAllWindows()

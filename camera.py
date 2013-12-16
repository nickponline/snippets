import cv2
import time

cv2.namedWindow("preview")
vc = cv2.VideoCapture(-1)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

counter = 0
while rval:
    rval, frame = vc.read()
    cv2.imshow("preview", frame)
    counter += 1
    print "Captured.", counter
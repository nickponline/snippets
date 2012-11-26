"""
 Face detection
"""

import itertools
import json
import json
import math
import md5
import os
import random
import sys
import time
import urllib
import pylab
import numpy

from cv2.cv import *
from cv2 import CascadeClassifier, waitKey, imread, imshow, cvtColor, equalizeHist, rectangle, Sobel, GaussianBlur

face_cascade_name = "haarcascade_frontalface_alt.xml";
eyes_cascade_name = "haarcascade_eye.xml";

face_cascade = CascadeClassifier(face_cascade_name)
eyes_cascade = CascadeClassifier(eyes_cascade_name)

image = imread("jaxons_class_crop.jpg")
colour_image = image
image = cvtColor(image, CV_BGR2GRAY)
image = equalizeHist(image)

objects = face_cascade.detectMultiScale(image, 1.1, 2, 0 | CV_HAAR_SCALE_IMAGE, (30, 30))

for x, y, w, h in objects:
	rectangle(image, (x, y), (x+w, y+h), (255, 255, 255))
	face_image = image[y:y+h,x:x+w]

	
imshow("Image", image)
waitKey(0)




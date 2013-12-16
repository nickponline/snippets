import cv2
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('sample.avi')
cv2.namedWindow("input")
while(True):
    f, img = cap.read()
    print f, img
    cv2.imshow("input", img)
    cv2.waitKey(1)
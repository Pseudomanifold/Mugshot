#!/usr/bin/env python2

import cv2

webcam = cv2.VideoCapture(0)

if webcam:
  gotFrame, frame = webcam.read()
else:
  gotFrame = False

classifier = cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml")

while gotFrame:

  gotFrame, frame = webcam.read()
  gray            = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  key             = cv2.waitKey(100)

  faces = classifier.detectMultiScale(gray,
                                      scaleFactor=1.2,
                                      minNeighbors=6,
                                      minSize=(30,30),
                                      flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

  for x,y,w,h in faces:
    cv2.rectangle(gray,(x,y),(x+w,y+h),(255,255,255),1)

  cv2.imshow("", gray)

  if key in [27, ord('q')]:
    break

webcam.release()

#!/usr/bin/env python2

import cv2
import datetime

webcam = cv2.VideoCapture(0)

if webcam:
  gotFrame, frame = webcam.read()
else:
  gotFrame = False

classifier   = cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml")
lastTime     = None
lastNumFaces = 0

while gotFrame:

  gotFrame, frame = webcam.read()
  gray            = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray            = cv2.equalizeHist(gray)

  faces = classifier.detectMultiScale(gray,
                                      scaleFactor=1.2,
                                      minNeighbors=4,
                                      minSize=(40,40),
                                      flags=cv2.CASCADE_SCALE_IMAGE)
  save = False

  if len(faces) > 0:
    currentTime = datetime.datetime.now()
    if lastTime:
      elapsedSeconds = (currentTime - lastTime).total_seconds()
    else:
      elapsedSeconds = 10

    if elapsedSeconds >= 10 or lastNumFaces != len(faces):
      save = True

    lastTime     = currentTime
    lastNumFaces = len(faces)

  for i,(x,y,w,h) in enumerate(faces):
    cv2.rectangle(gray,(x,y),(x+w,y+h),(255,255,255),1)
    if save:
      face     = frame[y:y+h,x:x+w]
      filename = lastTime.strftime("%Y%m%d-%H%M%S")+"-"+str(i)+".png"
      cv2.imwrite(filename, face)

  cv2.imshow("", gray)

  key = cv2.waitKey(200)
  if key in [27, ord('q')]:
    break

webcam.release()

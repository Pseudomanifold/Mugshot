#!/usr/bin/env python2
#
# mugshot.py: Creates automated mugshots of people near your computer
#             Inspired by Neal Stephenson's "Cryptonomicon"
#
# Copyright (C) 2015 Bastian Rieck 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import cv2
import datetime

parser = argparse.ArgumentParser(description="Creates automated mugshots of people near your computer")
parser.add_argument("--hide", help="Do not show the detected faces", action="store_true")

arguments = parser.parse_args()
webcam    = cv2.VideoCapture(0)

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

  if not arguments.hide:
    cv2.imshow("", gray)

  key = cv2.waitKey(200)
  if key in [27, ord('q')]:
    break

webcam.release()

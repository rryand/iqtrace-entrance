import threading

import cv2
import mss
import numpy

import threads.processors.face_recog as face_recog

class screenThread(threading.Thread):
  def __init__(self, previewName):
    threading.Thread.__init__(self)
    self.previewName = previewName
    self.is_active = True
    self.frame = None

  def run(self):
    print("Starting " + self.previewName)
    self.screenRun(self.previewName)

  def screenRun(self, name):
    with mss.mss() as sct:
      monitor = {"top": 40, "left": 0, "width": 600, "height": 360}

      while self.is_active:
        #last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))

        # Get faces from screen
        frame = face_recog.detectFaceFromStream(img)

        # Display the picture
        #cv2.imshow(name, frame)

        self.frame = frame

        #print("fps: {}".format(1 / (time.time() - last_time)))
      
      print("End screen read")


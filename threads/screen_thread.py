import threading

import cv2
import mss
import numpy

import threads.processors.face_recog as face_recog

class screenThread(threading.Thread):
  def __init__(self, previewName):
    threading.Thread.__init__(self)
    self.previewName = previewName
  def run(self):
    print("Starting " + self.previewName)
    screenRun(self.previewName)

def screenRun(name):
  with mss.mss() as sct:
    monitor = {"top": 40, "left": 0, "width": 600, "height": 640}

    while "Screen capturing":
      #last_time = time.time()

      # Get raw pixels from the screen, save it to a Numpy array
      img = numpy.array(sct.grab(monitor))

      # Get faces from screen
      frame = face_recog.detectFaceFromStream(img)

      # Display the picture
      cv2.imshow(name, frame)

      #print("fps: {}".format(1 / (time.time() - last_time)))

      # Press "q" to quit
      key = cv2.waitKey(25)
      if key & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break

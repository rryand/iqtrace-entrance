import threading

import cv2
import mss
import numpy

import threads.processors.face_recog as face_recog

class ScreenThread(threading.Thread):
  def __init__(self, previewName):
    threading.Thread.__init__(self)
    self.previewName = previewName
    self.frame = None
    self.face_frame = None
  
  def terminate(self):
    print("Terminating ", self.previewName)
    self._is_running = False

  def run(self):
    print("Starting " + self.previewName)
    self._is_running = True
    self.run_screen(self.previewName)

  def run_screen(self, name):
    process_frame = True
    with mss.mss() as sct:
      monitor = {"top": 40, "left": 0, "width": 600, "height": 360}

      while self._is_running:
        #print("running screen")
        #last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))

        # Get faces from screen
        if process_frame:
          (frame, face_frame) = face_recog.detectFaceFromStream(img)
        process_frame = not process_frame

        self.face_frame = face_frame

        # Display the picture
        #cv2.imshow(name, frame)

        self.frame = frame

        #print("fps: {}".format(1 / (time.time() - last_time)))
      
      print("Stopping screen read")
    
  def has_face_frame(self):
    return True if self.face_frame is not None else False
  
  def pop_face_frame(self):
    face_frame = self.face_frame
    self.face_frame = None
    return face_frame

  def write_temp(self, temp):
    y = 50
    cv2.putText(self.frame, f"Temp: {temp}", (50, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

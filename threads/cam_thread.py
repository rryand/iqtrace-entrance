import json
import threading

import cv2

import threads.processors.qr_detector as qr

def is_json(data):
  try:
    json_object = json.loads(data)
  except ValueError as e:
    print(False)
    return False
  print(True)
  return True

class CameraThread(threading.Thread):
  def __init__(self, previewName, camID):
    threading.Thread.__init__(self)
    self.previewName = previewName
    self.camID = camID
    self.frame = None
    self.qr_data = None

  # TODO: Make base class for camera threads
  def terminate(self):
    print("Terminating ", self.previewName)
    self._is_running = False

  def run(self):
    print("Starting " + self.previewName)
    self._is_running = True
    self.run_camera(self.previewName, self.camID)

  def run_camera(self, previewName, camID):
    #cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():
      #rval, frame = cam.read()
      print()
    else:
      print("ALERT: Camera is not open!")
      self._is_running = False
      #rval = False

    while self._is_running and not self.has_valid_qr_data():
      rval, frame = cam.read()
      (frame, data) = qr.detectQrCode(frame)
      self.qr_data = json.loads(data) if data is not None and is_json(data) else data
      print(type(self.qr_data))
      #cv2.imshow(previewName, frame)
      self.frame = frame
    
    print("Stopping camera")
      
    #cv2.destroyWindow(previewName)
  
  def has_valid_qr_data(self):
    return False if self.qr_data is None else True
  
  def pop_qr_data(self):
    data = self.qr_data
    self.qr_data = None
    return data

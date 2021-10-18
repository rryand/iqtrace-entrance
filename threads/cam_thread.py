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
  def __init__(self, preview_name, cam_id):
    threading.Thread.__init__(self)
    self.preview_name = preview_name
    self.cam_id = cam_id
    self.frame = None
    self.qr_data = None

  # TODO: Make base class for camera threads
  def terminate(self):
    print("Terminating " + self.preview_name)
    self._is_running = False

  def run(self):
    print("Starting " + self.preview_name)
    self._is_running = True
    self.run_camera(self.preview_name, self.cam_id)

  def run_camera(self, preview_name, camID):
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():
      #rval, frame = cam.read()
      print(f"{preview_name} is open.")
    else:
      print("ALERT: Camera is not open!")
      self._is_running = False
      #rval = False

    process_this_frame = True
    while self._is_running and not self.has_valid_qr_data():
      rval, frame = cam.read()
      if process_this_frame:
        (frame, data) = qr.detectQrCode(frame)
        self.qr_data = json.loads(data) if data is not None and is_json(data) else data
      process_this_frame = not process_this_frame
      self.frame = frame
    
    print("Stopping camera")
  
  def has_valid_qr_data(self):
    return False if self.qr_data is None else True
  
  def pop_qr_data(self):
    data = self.qr_data
    self.qr_data = None
    return data
  
  def write_data_to_frame(self, data: dict):
    data.pop('face_encoding')
    i = 0
    y0, dy = 50, 20
    for key, value in data.items():
      print(key, value)
      i += 1
      y = y0 + i*dy
      cv2.putText(self.frame, f"{key}: {value}", (50, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)


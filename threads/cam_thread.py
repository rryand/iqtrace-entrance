import threading

import cv2

import threads.processors.qr_detector as qr

class camThread(threading.Thread):
  def __init__(self, previewName, camID):
    threading.Thread.__init__(self)
    self.previewName = previewName
    self.camID = camID
    self.is_active = True
    self.frame = None

  def run(self):
    print("Starting " + self.previewName)
    self.camPreview(self.previewName, self.camID)

  def camPreview(self, previewName, camID):
    #cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():
      rval, frame = cam.read()
    else:
      self.is_active = False
      rval = False

    while self.is_active:
      frame = qr.detectQrCode(frame)
      #cv2.imshow(previewName, frame)
      self.frame = frame
      rval, frame = cam.read()
    
    print("End cam preview")
      
    #cv2.destroyWindow(previewName)

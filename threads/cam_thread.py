import threading

import cv2

import threads.processors.qr_detector as qr

class camThread(threading.Thread):
  def __init__(self, previewName, camID):
    threading.Thread.__init__(self)
    self.previewName = previewName
    self.camID = camID
  def run(self):
    print("Starting " + self.previewName)
    camPreview(self.previewName, self.camID)

def camPreview(previewName, camID):
  cv2.namedWindow(previewName)
  cam = cv2.VideoCapture(camID)
  if cam.isOpened():
    rval, frame = cam.read()
  else:
    rval = False

  while rval:
    frame = qr.detectQrCode(frame)
    cv2.imshow(previewName, frame)
    rval, frame = cam.read()
    key = cv2.waitKey(25)
    if key & 0xFF == ord("q"):  # exit on ESC
        break
  cv2.destroyWindow(previewName)

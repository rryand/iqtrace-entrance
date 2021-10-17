import numpy as np

import cv2

from threads.cam_thread import CameraThread
from threads.screen_thread import ScreenThread

# NOTE: Plug in PixyCam2 first before webcam

def get_qr_thread():
  return CameraThread("IQT QR Detector", 0)
  
def get_screen_thread():
  return ScreenThread("Screen")

def display(qr_frame, screen_frame):
  combined_frame = _build_frame(qr_frame, screen_frame)
  cv2.imshow("IQT Entrance", combined_frame)
  #print("displaying...")

def _build_frame(frame1, frame2):
  h1, w1 = frame1.shape[:2]
  h2, w2 = frame2.shape[:2]
  vis = np.zeros((h1 + h2, max(w1, w2), 4), np.uint8)
  vis[:h1, :w1, :3] = frame1
  vis[h1:h1+h2, :w2, :4] = frame2
  return vis

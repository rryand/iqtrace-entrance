import numpy as np

import cv2

from threads.cam_thread import camThread
from threads.screen_thread import screenThread

# NOTE: Plug in PixyCam2 first before webcam

qr_thread = camThread("IQT QR Detector", 0)
screen_thread = screenThread("Screen")

def display(qr_frame, screen_frame):
  h1, w1 = qr_frame.shape[:2]
  h2, w2 = screen_frame.shape[:2]
  vis = np.zeros((h1 + h2, max(w1, w2), 4), np.uint8)
  vis[:h1, :w1, :3] = qr_frame
  vis[h1:h1+h2, :w2, :4] = screen_frame
  cv2.imshow("IQT Entrance", vis)

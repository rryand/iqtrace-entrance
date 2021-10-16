import threading
import numpy as np

import cv2

from display import qr_thread, screen_thread

qr_thread.start()
screen_thread.start()

print("Active threads", threading.activeCount())

while True:
  cv2.namedWindow("IQT Entrance")

  if qr_thread.frame is not None and screen_thread.frame is not None:
    h1, w1 = qr_thread.frame.shape[:2]
    h2, w2 = screen_thread.frame.shape[:2]
    vis = np.zeros((h1 + h2, max(w1, w2), 4), np.uint8)
    vis[:h1, :w1, :3] = qr_thread.frame
    vis[h1:h1+h2, :w2, :4] = screen_thread.frame
    cv2.imshow("IQT Entrance", vis)

  key = cv2.waitKey(25)
  if key & 0xFF == ord("q"):
    qr_thread.is_active = False
    screen_thread.is_active = False
    cv2.destroyAllWindows()
    break

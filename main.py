import threading

import cv2

from display import qr_thread, screen_thread, display

def main():
  qr_thread.start()
  screen_thread.start()

  print("Active threads", threading.activeCount())

  while True:
    cv2.namedWindow("IQT Entrance")

    if qr_thread.frame is not None and screen_thread.frame is not None:
      display(qr_thread.frame, screen_thread.frame)

    key = cv2.waitKey(25)
    if key & 0xFF == ord("q"):
      qr_thread.is_active = False
      screen_thread.is_active = False
      cv2.destroyAllWindows()
      break

main()

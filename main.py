import threading
import time

import cv2

import api
from display import get_qr_thread, get_screen_thread, display

def main() -> None:
  qr_thread = get_qr_thread()
  screen_thread = get_screen_thread()
  _initialize_cameras(qr_thread, screen_thread)
  cv2.namedWindow("IQT Entrance")
  has_qr = False

  while True:
    #print("main loop")
    if qr_thread.frame is not None and screen_thread.frame is not None:
      display(qr_thread.frame, screen_thread.frame)
    
    if cv2.waitKey(25) & 0xFF == ord("q"):
      qr_thread.terminate()
      screen_thread.terminate()
      cv2.destroyAllWindows()
      break
    
    if qr_thread.has_valid_qr_data():
      qr_data = qr_thread.pop_qr_data()
      qr_thread.terminate()

      if (type(qr_data) == dict):
        print(qr_data['email'])
        user_data = api.get(f"/users?email={qr_data['email']}")
        print(user_data)
        print("after api get")

      # Facial recog
      screen_thread = get_screen_thread()
      screen_thread.start()

      # Temp
  
  print("End main()")

def _initialize_cameras(qr_thread, screen_thread) -> None:
  print("Initializing cameras")

  qr_thread.start()
  screen_thread.start()

  print("sleeping for 1 sec")
  time.sleep(1)

  screen_thread.terminate()

  print("Finished initializing cameras")
  print("Active threads", threading.activeCount())

main()

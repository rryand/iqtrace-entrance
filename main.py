import threading
import time

import cv2

import api
import face_verification as fv
from display import get_qr_thread, get_screen_thread, display

def main() -> None:
  qr_thread = get_qr_thread()
  screen_thread = get_screen_thread()
  user_data = None
  is_verified = False
  
  _initialize_cameras(qr_thread, screen_thread)
  cv2.namedWindow("IQT Entrance")

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
        user_data = api.get(f"/users?email={qr_data['email']}")
        face_encoding = user_data['face_encoding']

      # Facial recog
      screen_thread = get_screen_thread()
      screen_thread.start()
    
    if user_data is not None and len(face_encoding) > 0 and screen_thread.has_face_frame() and not is_verified:
      screen_thread.terminate()
      face_frame = screen_thread.pop_face_frame()
      cv2.imwrite('test2.jpg', screen_thread.frame[:,:,:3])
      screen_image = cv2.imread('test2.jpg')
      is_verified = fv.verify_face(face_encoding, screen_image, tolerance=0.5)

    #if is_verified:
    
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

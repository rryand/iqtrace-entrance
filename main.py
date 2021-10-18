import threading
import time
from datetime import datetime

import cv2

import api
import irt
import face_verification as fv
from display import get_qr_thread, get_screen_thread, display

def _initialize_cameras(qr_thread, screen_thread) -> None:
  print("Initializing cameras")

  qr_thread.start()
  screen_thread.start()

  print("sleeping for 1 sec")
  time.sleep(1)

  screen_thread.terminate()

  print("Finished initializing cameras")
  print("Active threads", threading.activeCount())

def main() -> None:
  ENTRANCE_ROOM_NUM = 1

  qr_thread = get_qr_thread()
  screen_thread = get_screen_thread()
  user_data = None
  is_verified = False
  is_done = False
  is_temp_measured = False
  
  _initialize_cameras(qr_thread, screen_thread)
  cv2.namedWindow("IQT Entrance")

  while True:
    if qr_thread.frame is not None and screen_thread.frame is not None:
      display(qr_thread.frame, screen_thread.frame)

    # PRESS Q TO QUIT
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
        qr_thread.write_data_to_frame(user_data.copy())
        display(qr_thread.frame, screen_thread.frame)

      screen_thread = get_screen_thread()
      screen_thread.start()
    
    if user_data is not None and len(face_encoding) > 0 and screen_thread.has_face_frame() and not is_verified:
      face_frame = screen_thread.pop_face_frame()
      cv2.imwrite('test2.jpg', screen_thread.frame[:,:,:3])
      screen_image = cv2.imread('test2.jpg')
      is_verified = fv.verify_face(face_encoding, screen_image, tolerance=0.3)

    if is_verified:
      screen_thread.terminate()
      temp = irt.read_temperature()
      print(f"Final temp: {temp}")
      screen_thread.write_temp(temp)
      is_temp_measured = True
    
    if is_temp_measured:
      user_data['temp'] = temp
      api.patch(f"/user-temp?email={qr_data['email']}&temp={temp}")

      timelog = {
        'user_email': user_data['email'],
        'room_number': ENTRANCE_ROOM_NUM,
        'timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
      }
      print(timelog['timestamp'])
      api.post(f"/timelog", timelog)

      is_temp_measured = False
      is_done = True
      

    if is_verified and is_done:
      print("Wrapping up...")
      is_verified = False
      is_done = False
      user_data = None
      qr_thread = get_qr_thread()
      qr_thread.start()
  
  print("End main()")

main()

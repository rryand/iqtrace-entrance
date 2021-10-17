import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def detectFaceFromStream(frame):
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, 1.1, 4)

  for x, y, w, h in faces:
    #cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    face_frame = _get_face_frame(frame, x, y, w, h)

  if len(faces) <= 0:
    face_frame = None

  return (frame, face_frame)

def _get_face_frame(frame, x, y, w, h):
  return frame[x:x+w, y:y+h, :4]

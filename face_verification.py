import cv2
import face_recognition
import numpy

# def saveImageFromFile(image):
#   image_bytes = image.read()
#   decoded = cv2.imdecode(numpy.frombuffer(image_bytes, numpy.uint8), -1)

#   print("OpenCV:\n", decoded)

#   cv2.imwrite("output.jpg", decoded)

def verify_face(known_encoding, unknown_frame, tolerance=0.6):
  try:
    known_encoding2 = numpy.array(known_encoding)
    unknown_encoding = face_recognition.face_encodings(unknown_frame)[0]

    result = face_recognition.compare_faces([known_encoding2], unknown_encoding, tolerance)[0]
  except IndexError:
    result = False

  return result

def compare_faces(unknown_image_file, user_image_file, tolerance=0.6):
  known_image = cv2.imread(user_image_file)
  unknown_image = cv2.imread(unknown_image_file)

  known_encoding = face_recognition.face_encodings(known_image)[0]
  unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
  print(face_recognition.face_distance([known_encoding], unknown_encoding))

  result = face_recognition.compare_faces([known_encoding], unknown_encoding, tolerance)

  _displayFaceComparison(result, unknown_image, known_image)
  return result

def _displayFaceComparison(result, unknown_image, known_image):
  unknown_face = face_recognition.face_locations(unknown_image)[0]
  top, right, bottom, left = unknown_face
  unknown_image = unknown_image[top:bottom, left:right]

  known_face = face_recognition.face_locations(known_image)[0]
  top, right, bottom, left = known_face
  known_image = known_image[top:bottom, left:right]

  h1, w1 = unknown_image.shape[:2]
  h2, w2 = known_image.shape[:2]

  vis = numpy.zeros((max(h1, h2), w1+w2,3), numpy.uint8)
  vis[:h1, :w1,:3] = unknown_image
  vis[:h2, w1:w1+w2,:3] = known_image

  font = cv2.FONT_HERSHEY_DUPLEX
  cv2.putText(vis, str(result), (10, max(h1, h2) - 10), font, 1.0, (0, 0, 255), 2)

  cv2.imwrite("output.jpg", vis)

  cv2.imshow("Face Recognition", vis)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

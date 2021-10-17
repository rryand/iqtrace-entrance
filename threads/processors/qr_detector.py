import cv2

qr_detector = cv2.QRCodeDetector()

# TODO: Optimize
def detectQrCode(frame) -> tuple:
  data, bbox, qr_image = qr_detector.detectAndDecode(frame)

  if(len(data) > 0):
    cv2.putText(
      frame, 
      data, 
      (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), 
      cv2.FONT_HERSHEY_SIMPLEX, 
      0.6, 
      (0, 255, 0), 
      2
    )
    print(data)
    return (frame, data)
  
  return (frame, None)
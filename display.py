from threads.cam_thread import camThread
from threads.screen_thread import screenThread

# NOTE: Plug in PixyCam2 first before webcam

qr_thread = camThread("IQT QR Detector", 0)
screen_thread = screenThread("Screen")

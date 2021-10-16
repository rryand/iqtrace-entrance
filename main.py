import threading

from display import qr_thread, screen_thread

qr_thread.start()
screen_thread.start()

print("Active threads", threading.activeCount())
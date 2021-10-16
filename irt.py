import time

from smbus2 import SMBus
from mlx90614 import MLX90614

_offset = 7.0
interval = 0.5
loops = 6

def getTemperature() -> float:
  object_temp = 0

  for i in range(loops):
    time.sleep(interval)

    try:
      bus = SMBus(1)
      sensor = MLX90614(bus, address=0x5A)

      measured_temp = sensor.get_object_1() + _offset

      if (measured_temp > object_temp):
        object_temp = measured_temp
    except OSError:
      pass
    except KeyboardInterrupt:
      bus.close()
      break
    else:
      print(
        f"Measured Temp: {measured_temp} | "
        f"Object Temp: {object_temp}"
      )

  return object_temp

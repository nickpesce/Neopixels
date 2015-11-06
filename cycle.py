import np
import time

while(True):
    for h in range(0, 10000):
        np.set_all_pixels_hsv(h/10000.0, 1, 1)
        np.show()
        time.sleep(.05)
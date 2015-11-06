import np
import time

off = 0

while(True):
    for n in range(0, 60):
        np.set_pixel_hsv(n, ((n*off)/60.0)%1, 1, 1)
    off+=.1
    np.show()
    time.sleep(.05)
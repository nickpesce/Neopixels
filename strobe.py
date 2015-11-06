import np
import time

np.brightness(1)
while(True):
    np.set_all_pixels(255, 255, 255)
    np.show()
    time.sleep(.1)
    np.off()
    time.sleep(.1)
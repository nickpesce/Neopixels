import np
import time
import random

while(True):
    for n in range(0, 60):
        np.set_pixel(n, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    np.show();
    time.sleep(.1)
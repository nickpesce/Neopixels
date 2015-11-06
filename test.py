#!/usr/bin/env python

import np
import time

for n in range(0, 60):
    np.set_pixel(n, 255, 255, 0)
    np.show()
    time.sleep(.5);



time.sleep(10000)
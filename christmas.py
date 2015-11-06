#!/usr/bin/env python
import np
import time
import math

for n in range(0, 60):
    x = math.fabs((30 - n)/30.0)
    np.set_pixel(n, int(255-(x*255)), int(x*255), 0)
	
while(True):
    first = np.get_pixel(0)
    for n in range(0, 59):
        np.set_pixel(n, *np.get_pixel(n+1))
        np.set_pixel(59, *first)
    np.show()
    time.sleep(.2)



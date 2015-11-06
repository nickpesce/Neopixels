import np
import time

x = 0
dx = .1
while(True):
    np.off()
    np.set_pixel_hsv(int(x), (x/60.0)%1, 1, 1)
    np.set_pixel_hsv(int(60-x), ((60-x)/60.0)%1, 1, 1)
    x+=dx
    if(x+dx >=60 or x+dx <0):
        dx = -dx
    np.show()
    time.sleep(.001)
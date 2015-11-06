import np, time, random, math, sys, getopt

running = False
def start(args):
    if len(args)<1:
        print 'sudo python neopixels.py <effect> -s <speed>'
        sys.exit(2)
    effect = effects[args[0]]
    speed = None
    r = None
    g = None
    b = None
    try:
        opts, args = getopt.getopt(args[1:], "s:r:g:b:")
    except getopt.GetoptError:
        print 'sudo python neopixels.py <effect> -s <speed>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-s':
            speed = float(arg)
        elif opt == '-r':
            r = int(arg)
        elif opt == '-g':
            g = int(arg)
        elif opt == '-b':
            b = int(arg)

    hasSpeed = False
    hasColor = False
    if not speed is None:
        hasSpeed = True
    if r is not None and b is not None and g is not None:
        hasColor = True

    if hasSpeed and hasColor:
        effect(speed = speed, r = r, g = g, b = b)
    elif hasSpeed:
        effect(speed = speed)
    elif hasColor:
        effect(r = r, g = g, b = b)
    else:
        effect()

    
def slide(speed = 1):
    off = 0
    while(True):
        for n in range(0, 60):
            np.set_pixel_hsv(n, ((n+off)/60.0)%1, 1, 1)
        off+=.1
        np.show()
        time.sleep(.05/speed)
        
def bounce(speed=1):
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
        time.sleep(.001/speed)

def christmas(speed=1):
    for n in range(0, 60):
        x = math.fabs((30 - n)/30.0)
        np.set_pixel(n, int(255-(x*255)), int(x*255), 0)
            
    while(True):
        first = np.get_pixel(0)
        for n in range(0, 59):
            np.set_pixel(n, *np.get_pixel(n+1))
            np.set_pixel(59, *first)
        np.show()
        time.sleep(.2/speed)
        
def cycle(speed=1):
    global running
    running = True
    while(running):
        for h in range(0, 10000):
            np.set_all_pixels_hsv(h/10000.0, 1, 1)
            np.show()
            time.sleep(.05/speed)

def rave(speed=1):
    global running
    running = True
    while(running):
        for n in range(0, 60):
            np.set_pixel(n, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        np.show();
        time.sleep(.1/speed)

def strobe(speed=1, r=255, g=255, b=255):
    while(True):
        np.set_all_pixels(r, g, b)
        np.show()
        time.sleep(.1/speed)
        np.off()
        time.sleep(.1/speed)
        
def throb(speed=1, r=255, b=255, g=255):
    np.set_all_pixels(r, g, b)
    brightness = 0
    db = .01
    while(True):
        np.brightness(brightness)
        np.show()
        if brightness + db > 1 or brightness + db < 0:
            db = -db
        brightness += db
        time.sleep(.01/speed)

def on(r = 255, g = 255, b = 255):
    np.set_all_pixels(r, g, b)
    np.show()
    while True:
        time.sleep(1)

def disco(speed=1):
    off = 0
    while(True):
        for n in range(0, 60):
            np.set_pixel_hsv(n, ((n*off)/60.0)%1, 1, 1)
        off+=.1
        np.show()
        time.sleep(.05/speed)

def bounce(speed=1):
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
        time.sleep(.001/speed)

def chase(speed = 1):
    hue = 0;
    while True:
        for n in range(0, 60):
            np.set_pixel_hsv(n, hue, 1, 1)
            np.show()
            time.sleep(.05/speed)
        hue += .2
        hue %= 1
    
def stop():
    np.off()

effects = {'cycle' : cycle,
           'slide' : slide,
           'bounce' : bounce,
           'christmas' : christmas,
           'rave' : rave,
           'strobe' : strobe,
           'disco' : disco,
           'on' : on,
           'chase' : chase,
           'throb' : throb,
           'stop' : stop
    }

if __name__ == "__main__":
    start(sys.argv[1:])

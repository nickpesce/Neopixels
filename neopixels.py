import np, time, random, math, sys, getopt, threading

__author__="Nick Pesce"
__email__="npesce@terpmail.umd.edu"

global stop_event

def start(args, stop=threading.Event()):
    """Determines effect  parameters to run with.

    Param args: The arguments passed in without the script name.
    args:
        - name of effect (Must be first)
        - -r [0, 255] -g [0, 255] -b [0, 255]. All or none.
        - -s (0, infinity) speed. multiple of normal.
    Param stop: thread stop event."""
    global stop_event
    stop_event = stop
    if len(args)<1:
        return help()
        sys.exit(2)
    speed = None
    r = None
    g = None
    b = None
    try:
        #Separates the passed in arguments to option, argument tuples.
        opts, rest = getopt.getopt(args[1:], "s:r:g:b:h")
    except getopt.GetoptError:
        return help()
        sys.exit(2)
    for opt, val in opts:
        #assign variables to passed in values
        if opt == '-s':
            speed = float(val)
        elif opt == '-r':
            r = int(val)
        elif opt == '-g':
            g = int(val)
        elif opt == '-b':
            b = int(val)
        elif opt == '-h':
            return help()

    #Determine which parameters were passed.
    hasSpeed = False
    hasColor = False
    if not speed is None:
        hasSpeed = True
    if r is not None and b is not None and g is not None:
        hasColor = True

    #Call with the correct parameters based on what was passed in.
    # If parameters dod not match, an error will be thrown.
    try:
        effect = effects[args[0]]
        if hasSpeed and hasColor:
            effect(speed = speed, r = r, g = g, b = b)
        elif hasSpeed:
            effect(speed = speed)
        elif hasColor:
            effect(r = r, g = g, b = b)
        else:
            effect()
    except:
        return help()

def help():
    return """sudo python neopixels.py <effect> [-s speed] [-r red -g green -b blue]
Effects:\n    - """ + ("\n    - ".join(effects.keys()))

    
def slide(speed = 1):
    """The full color spectrum is shown and it "slides"/translates across the string

    Param speed: How fast it slides. Scales the default speed."""
    global stop_event
    off = 0
    while(not stop_event.is_set()):
        for n in range(0, 60):
            np.set_pixel_hsv(n, ((n+off)/60.0)%1, 1, 1)
        off+=.1
        np.show()
        stop_event.wait(.05/speed)
        
def bounce(speed=1):
    """Two pixels start on either end and move along the string changing color.
    When the end is hit, they change  direction

    Param speed: Scales the default speed."""
    global stop_event
    x = 0
    dx = .1
    while(not stop_event.is_set()):
        np.off()
        np.set_pixel_hsv(int(x), (x/60.0)%1, 1, 1)
        np.set_pixel_hsv(int(60-x), ((60-x)/60.0)%1, 1, 1)
        x+=dx
        if(x+dx >=60 or x+dx <0):
            dx = -dx
        np.show()
        stop_event.wait(.01/speed)

def christmas(speed=1):
    """Lights up green and red. Pattern "slides" along the string.

    Param speed: Scales the default speed"""

    global stop_event
    for n in range(0, 60):
        x = math.fabs((30 - n)/30.0)
        np.set_pixel(n, int(255-(x*255)), int(x*255), 0)
            
    while(not stop_event.is_set()):
        first = np.get_pixel(0)
        for n in range(0, 59):
            np.set_pixel(n, *np.get_pixel(n+1))
            np.set_pixel(59, *first)
        np.show()
        stop_event.wait(.2/speed)
        
def cycle(speed=1):
    """Cycles through the color spectrum. Entire string is the same color.
    
    Param speed: Scales the default speed."""

    global stop_event
    while not stop_event.is_set():
        for h in range(0, 1000):
            if stop_event.is_set():
                break
            np.set_all_pixels_hsv(h/1000.0, 1, 1)
            np.show()
            stop_event.wait(.05/speed)

def rave(speed=1):
    """Each individual light displays a different random color, changing rapidly.

    Param speed: Scales the default speed."""

    global stop_event
    while(not stop_event.is_set()):
        for n in range(0, 60):
            np.set_pixel(n, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        np.show();
        stop_event.wait(.1/speed)

def strobe(speed=1, r=255, g=255, b=255):
    """Entire string flashes rapidly.
    
    Param speed: Scales the default speed.
    Param r, g, b: Default white. RGB values for light color. [0, 255]"""
    
    global stop_event
    while(not stop_event.is_set()):
        np.set_all_pixels(r, g, b)
        np.show()
        stop_event.wait(.1/speed)
        np.off()
        stop_event.wait(.1/speed)
        
def throb(speed=1, r=255, b=255, g=255):
    """Entire string cycles through brightness levels. Starts off, gradually gets brighters, the darker, and repeats.
    
    Param speed: Scales the default speed.
    Param r, g, b: Default white. RGB values for light color. [0, 255]"""

    global stop_event
    np.set_all_pixels(r, g, b)
    brightness = 0
    db = .01
    while(not stop_event.is_set()):
        np.brightness(brightness)
        np.show()
        if brightness + db > 1 or brightness + db < 0:
            db = -db
        brightness += db
        stop_event.wait(.01/speed)

def on(r = 255, g = 255, b = 255):
    """Turns the entire string on.
    Param r, g, b: Default white. RGB values for light color. [0, 255]"""

    global stop_event
    np.set_all_pixels(r, g, b)
    np.show()
    while not stop_event.is_set():
        time.sleep(1)

def disco(speed=1):
    """Pattern formed when the color spectrum is repeated and condensed, then reversed
    
    Param speed: Scales the default speed."""

    global stop_event
    off = 0
    while not stop_event.is_set():
        for n in range(0, 60):
            np.set_pixel_hsv(n, ((n*off)/60.0)%1, 1, 1)
        off+=.1
        np.show()
        stop_event.wait(.05/speed)

def chase(speed = 1):
    """Each light sequentially lights up a color untill the string is filled with that color,
    then it is repeated with the next color. Each color is .2 hue away in HSV.

    Param speed: Scales the default speed."""

    global stop_event
    hue = 0;
    while not stop_event.is_set():
        for n in range(0, 60):
            if stop_event.is_set():
                break
            np.set_pixel_hsv(n, hue, 1, 1)
            np.show()
            stop_event.wait(.05/speed)
        hue += .2
        hue %= 1
    
def stop():
    """Turns the string off."""
    np.off()

#Maps string names to functions
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
    error = start(sys.argv[1:])
    if not error is None:
        print error
        sys.exit(2)

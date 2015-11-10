import np, time, random, math, sys, getopt, threading

__author__="Nick Pesce"
__email__="npesce@terpmail.umd.edu"

stop_event = None
t = None

def start(args, stop = threading.Event()):
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
        return (help(), None)
        sys.exit(2)
    speed = None
    c = None
    try:
        #Separates the passed in arguments to option, argument tuples.
        opts, rest = getopt.getopt(args[1:], "s:c:h")
    except getopt.GetoptError, e:
        return (help(), None)
        sys.exit(2)
    for opt, val in opts:
        try:
            #assign variables to passed in values
            if opt == '-s':
                speed = float(val)
            elif opt == '-c':
                if ";" in val:
                    c = get_int_tuple_tuple(val)
                else:
                    c = get_int_tuple(val)
            elif opt == '-h':
                return (help(), None)
        except:
            return (("flag " + opt + " with value " + val + " is not valid!"), None) 

    #Call with the correct parameters based on what was passed in.
    # If parameters dod not match, an error will be thrown.
    try:
        effect = effects[args[0]]
        if effect == each:
            each(c)
            return (None, None)
        global t
        t = threading.Thread(target=run_effect, args=(effect, c, speed))
        t.daemon = True
        t.start()
        return (args[0] + " started!", t)
    except Exception, e:
        return (help()+str(e), None)

def run_effect(effect, c, speed):
    #Determine which parameters were passed.
    hasSpeed = False
    hasColor = False
    if not speed is None:
        hasSpeed = True
    if not c is None:
        hasColor = True
        
    if hasSpeed and hasColor:
        effect(speed = speed, color = c)
    elif hasSpeed:
        effect(speed = speed)
    elif hasColor:
        effect(color = c)
    else:
        effect()


def help():
    return """sudo python neopixels.py <effect> [-s speed] [-c rgb tuple]
Effects:\n    - """ + ("\n    - ".join(effects.keys()))

    
def slide(speed = 1):
    """The full color spectrum is shown and it "slides"/translates across the string

    Param speed: How fast it slides. Scales the default speed."""
    global stop_event
    off = 0
    while(not stop_event.is_set()):
        for n in range(0, np.LED_COUNT):
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
        np.set_pixel_hsv(int(x), (x/float(np.LED_COUNT))%1, 1, 1)
        np.set_pixel_hsv(int(np.LED_COUNT-x), ((np.LED_COUNT-x)/float(np.LED_COUNT))%1, 1, 1)
        x+=dx
        if(x+dx >=np.LED_COUNT or x+dx <0):
            dx = -dx
        np.show()
        stop_event.wait(.01/speed)

def christmas(speed=1):
    """Lights up green and red. Pattern "slides" along the string.

    Param speed: Scales the default speed"""

    global stop_event
    for n in range(0, np.LED_COUNT):
        x = math.fabs((np.LED_COUNT/2 - n)/float(np.LED_COUNT/2))
        np.set_pixel(n, int(255-(x*255)), int(x*255), 0)
            
    while(not stop_event.is_set()):
        first = np.get_pixel(0)
        for n in range(0, np.LED_COUNT-1):
            np.set_pixel(n, *np.get_pixel(n+1))
            np.set_pixel(np.LED_COUNT-1, *first)
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
        for n in range(0, np.LED_COUNT):
            np.set_pixel(n, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        np.show();
        stop_event.wait(.1/speed)

def strobe(speed=1, color = (255, 255, 255)):
    """Entire string flashes rapidly.
    
    Param speed: Scales the default speed.
    Param r, g, b: Default white. RGB values for light color. [0, 255]"""
    
    global stop_event
    while(not stop_event.is_set()):
        np.set_all_pixels(color[0], color[1], color[2])
        np.show()
        stop_event.wait(.1/speed)
        np.off()
        stop_event.wait(.1/speed)
        
def throb(speed=1, color=(255, 255, 255)):
    """Entire string cycles through brightness levels. Starts off, gradually gets brighters, the darker, and repeats.
    
    Param speed: Scales the default speed.
    Param r, g, b: Default white. RGB values for light color. [0, 255]"""

    global stop_event
    np.set_all_pixels(color[0], color[1], color[2])
    brightness = 0
    db = .01
    while(not stop_event.is_set()):
        np.brightness(brightness)
        np.show()
        if brightness + db > 1 or brightness + db < 0:
            db = -db
        brightness += db
        stop_event.wait(.01/speed)

def on(color = (255, 255, 255)):
    """Turns the entire string on.
    Param r, g, b: Default white. RGB values for light color. [0, 255]"""

    np.set_all_pixels(color[0], color[1], color[2])
    np.show()

def disco(speed=1):
    """Pattern formed when the color spectrum is repeated and condensed, then reversed
    
    Param speed: Scales the default speed."""

    global stop_event
    off = 0
    while not stop_event.is_set():
        for n in range(0, np.LED_COUNT):
            np.set_pixel_hsv(n, ((n*off)/float(np.LED_COUNT))%1, 1, 1)
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
        for n in range(0, np.LED_COUNT):
            if stop_event.is_set():
                break
            np.set_pixel_hsv(n, hue, 1, 1)
            np.show()
            stop_event.wait(.05/speed)
        hue += .2
        hue %= 1
    
def each(each):
    """Lights the string according to the defined colors for each pixel passed in.
    
    Param each: List of tuples containing r, g, b values for each respective pixel in order."""
    
    np.set_pixels(each)
    np.show()

def stop():
    """Turns the string off."""
    np.off()
    
def get_int_tuple(arg):
    """Takes a string representation of a tuple filled with ints and returns an actual
    tuple filled with ints"""
    
    return tuple(map(int, arg[1:-1].split(",")))

def get_int_tuple_tuple (args):
    """Takes a string representation of multiple int tuples separated by spaces and returns a tuple of tuples."""
    
    return tuple(map(get_int_tuple, args.split(";")))
    
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
           'stop' : stop,
           'each' : each
    }

if __name__ == "__main__":
    response = start(sys.argv[1:])[0]
    if not response is None:
        print response
    raw_input("Press any enter to stop...")
    stop_event.set()
    if t is not None:
        t.join()

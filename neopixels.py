import np, time, random, math, sys, getopt, threading

__author__="Nick Pesce"
__email__="npesce@terpmail.umd.edu"

FLAG_RETURN = int('0b01', 2)
FLAG_STAY_CONNECTED = int('0b10', 2)
stop_event = None
t = None

def start(args, stop = threading.Event()):
    """Determines effect  parameters to run with.

    Param args: The arguments passed in without the script name.
    args:
        - name of effect (Must be first)
        - -c ([0, 255],[0, 255],[0, 255]). Set the color.
        - -s (0, infinity) speed. multiple of normal.
        - -e keep the stream open. Only use for quickly repeated commands throught control.py
        - -r Prevents output from being sent back when using control.py
    Param stop: thread stop event."""
    global stop_event
    stop_event = stop
    if len(args)<1:
        return (help(), 0, None, False)
        sys.exit(2)
    speed = None
    c = None
    flags = 0;
    try:
        #Separates the passed in arguments to option, argument tuples.
        opts, rest = getopt.gnu_getopt(args[1:], "s:c:h:e:r")
    except getopt.GetoptError, e:
        return ("Invalid Arguments:\n"+help(), 0, None, False)
        sys.exit(2)
    rest = combine_colors_in_list(rest)
    for word in rest:
        if speeds.has_key(word):
            speed = speeds[word]
        elif colors.has_key(word):
            c = colors[word]
    for opt, val in opts:
        try:
            #assign variables to passed in values
            if opt == '-s':
                speed = float(val)
            elif opt == '-c':
                if ";" in val:
                    c = get_int_tuple_tuple(val)
                elif "(" in val:
                    c = get_int_tuple(val)
                elif colors.has_key(val):
                    c = colors[val]
            elif opt == '-h':
                return (help(), 0, None, False)
            elif opt == '-r':
                flags += FLAG_RETURN
            elif opt == '-e':
                flags += FLAG_STAY_CONNECTED
        except:
            return (("flag " + opt + " with value " + val + " is not valid!"), 0, None, False) 

    #Call with the correct parameters based on what was passed in.
    # If parameters do not match, an error will be thrown.
    try:
        effect = effects[args[0].lower()]
        if effect == each:
            each(c)
            return ("each started!", flags, None, True)
        global t
        t = threading.Thread(target=run_effect, args=(effect, c, speed))
        t.daemon = True
        t.start()
        return (args[0] + " started!", flags, t, True)
    except Exception, e:
        return (help(), 0, None, False)

def combine_colors_in_list(list):
    """Takes a list of strings, and combines adjacent strings that are not known to be speeds"""
    ret = []
    cat = None
    for i in range(0, len(list)):
        if speeds.has_key(list[i].lower()):
            if not cat is None:
                ret.append(cat)
                cat = None
            ret.append(list[i].lower())
        else:
            if cat is None:
                cat = list[i].lower()
            else:
                cat += " " + list[i].lower()
    if not cat is None:
        ret.append(cat)
    return ret

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

def is_effect(name):
    return name.split(' ', 1)[0] in effects

def help():
    return """Effects:\n    ~ """ + ("\n    ~ ".join("%s %s" % tup for tup in command_help.items()))

    
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
    np.brightness(1)

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

def drip(color=(0, 200, 255), speed=1):
    dullness = [1.0]*np.LED_COUNT
    while not stop_event.is_set():
        for n in range(0, np.LED_COUNT):
            np.set_pixel(n, int(color[0]/dullness[n]), int(color[1]/dullness[n]), int(color[2]/dullness[n]))
            dullness[n] -= random.random()/20
            if dullness[n]<=1 or random.randint(0, int(dullness[n]*20)) == 0:
                dullness[n] = (random.random()*2)+4
        np.show()
        stop_event.wait(.05/speed)

def christmas_lights():
    lights = []
    for n in range(0, np.LED_COUNT):
        seq = n%5
        if seq == 0:
            lights.append((100, 0, 0))
        elif seq == 1:
            lights.append((100, 0, 50))
        elif seq == 2:
            lights.append((0, 100, 0))
        elif seq == 3:
            lights.append((150, 100, 0))
        elif seq == 4:
            lights.append((0, 0, 100))
    each(tuple(lights)) 

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
           'off' : stop,
           'each' : each,
           'drip' : drip,
           'christmas_lights' : christmas_lights
    }

command_help = {
        'cycle' : '[-s speed]',
        'slide' : '[-s speed]',
        'bounce' : '[-s speed]',
        'christmas' : '[-s speed]',
        'rave' : '[-s speed]',
        'strobe' : '[-c (r,g,b)] [-s speed]',
        'disco' : '[-s speed]',
        'on' : '[-c (r,g,b)]',
        'chase' : '[-s speed]',
        'throb' : '[-c (r,g,b)] [-s speed]',
        'off' : 'alias: stop',
        'drip' : '[-c (r,g,b)] [-s speed]',
        'christmas_lights' : '',
        'each' : '[-c ((r,g,b),...)]'
    }

colors = {
        'maroon' : (128,0,0),
        'dark red' : (139,0,0),
        'brown' : (165,42,42),
        'firebrick' : (178,34,34),
        'crimson' : (220,20,60),
        'red' : (255,0,0),
        'tomato' : (255,99,71),
        'coral' : (255,127,80),
        'indian red' : (205,92,92),
        'light coral' : (240,128,128),
        'dark salmon' : (233,150,122),
        'salmon' : (250,128,114),
        'light salmon' : (255,160,122),
        'orange red' : (255,69,0),
        'dark orange' : (255,140,0),
        'orange' : (255,165,0),
        'gold' : (255,215,0),
        'dark golden rod' : (184,134,11),
        'golden rod' : (218,165,32),
        'pale golden rod' : (238,232,170),
        'dark khaki' : (189,183,107),
        'khaki' : (240,230,140),
        'olive' : (128,128,0),
        'yellow' : (255,255,0),
        'yellow green' : (154,205,50),
        'dark olive green' : (85,107,47),
        'olive drab' : (107,142,35),
        'lawn green' : (124,252,0),
        'chartreuse' : (127,255,0),
        'green yellow' : (173,255,47),
        'dark green' : (0,100,0),
        'green' : (0,128,0),
        'forest green' : (34,139,34),
        'lime' : (0,255,0),
        'lime green' : (50,205,50),
        'light green' : (144,238,144),
        'pale green' : (152,251,152),
        'dark sea green' : (143,188,143),
        'medium spring green' : (0,250,154),
        'spring green' : (0,255,127),
        'sea green' : (46,139,87),
        'medium aqua marine' : (102,205,170),
        'medium sea green' : (60,179,113),
        'light sea green' : (32,178,170),
        'dark slate gray' : (47,79,79),
        'teal' : (0,128,128),
        'dark cyan' : (0,139,139),
        'aqua' : (0,255,255),
        'cyan' : (0,255,255),
        'light cyan' : (224,255,255),
        'dark turquoise' : (0,206,209),
        'turquoise' : (64,224,208),
        'medium turquoise' : (72,209,204),
        'pale turquoise' : (175,238,238),
        'aqua marine' : (127,255,212),
        'powder blue' : (176,224,230),
        'cadet blue' : (95,158,160),
        'steel blue' : (70,130,180),
        'corn flower blue' : (100,149,237),
        'deep sky blue' : (0,191,255),
        'dodger blue' : (30,144,255),
        'light blue' : (173,216,230),
        'sky blue' : (135,206,235),
        'light sky blue' : (135,206,250),
        'midnight blue' : (25,25,112),
        'navy' : (0,0,128),
        'dark blue' : (0,0,139),
        'medium blue' : (0,0,205),
        'blue' : (0,0,255),
        'royal blue' : (65,105,225),
        'blue violet' : (138,43,226),
        'indigo' : (75,0,130),
        'dark slate blue' : (72,61,139),
        'slate blue' : (106,90,205),
        'medium slate blue' : (123,104,238),
        'medium purple' : (147,112,219),
        'dark magenta' : (139,0,139),
        'dark violet' : (148,0,211),
        'dark orchid' : (153,50,204),
        'medium orchid' : (186,85,211),
        'purple' : (128,0,128),
        'thistle' : (216,191,216),
        'plum' : (221,160,221),
        'violet' : (238,130,238),
        'magentafuchsia' : (255,0,255),
        'fuchsia' : (255,0,255),
        'orchid' : (218,112,214),
        'medium violet red' : (199,21,133),
        'pale violet red' : (219,112,147),
        'deep pink' : (255,20,147),
        'hot pink' : (255,105,180),
        'light pink' : (255,182,193),
        'pink' : (255,192,203),
        'antique white' : (250,235,215),
        'beige' : (245,245,220),
        'bisque' : (255,228,196),
        'blanched almond' : (255,235,205),
        'wheat' : (245,222,179),
        'corn silk' : (255,248,220),
        'lemon chiffon' : (255,250,205),
        'light golden rod yellow' : (250,250,210),
        'light yellow' : (255,255,224),
        'saddle brown' : (139,69,19),
        'sienna' : (160,82,45),
        'chocolate' : (210,105,30),
        'peru' : (205,133,63),
        'sandy brown' : (244,164,96),
        'burly wood' : (222,184,135),
        'tan' : (210,180,140),
        'rosy brown' : (188,143,143),
        'moccasin' : (255,228,181),
        'navajo white' : (255,222,173),
        'peach puff' : (255,218,185),
        'misty rose' : (255,228,225),
        'lavender blush' : (255,240,245),
        'linen' : (250,240,230),
        'old lace' : (253,245,230),
        'papaya whip' : (255,239,213),
        'sea shell' : (255,245,238),
        'mint cream' : (245,255,250),
        'slate gray' : (112,128,144),
        'light slate gray' : (119,136,153),
        'light steel blue' : (176,196,222),
        'lavender' : (230,230,250),
        'floral white' : (255,250,240),
        'alice blue' : (240,248,255),
        'ghost white' : (248,248,255),
        'honeydew' : (240,255,240),
        'ivory' : (255,255,240),
        'azure' : (240,255,255),
        'snow' : (255,250,250),
        'black' : (0,0,0),
        'dim gray' : (105,105,105),
        'dim grey' : (105, 105, 105),
        'gray' : (128,128,128),
        'grey' : (128,128,128),
        'dark gray' : (169,169,169),
        'dark grey' : (169,169,169),
        'silver' : (192,192,192),
        'light grey' : (211,211,211),
        'light gray' : (211,211,211),
        'gainsboro' : (220,220,220),
        'white smoke' : (245,245,245),
        'white' : (255,255,255),
        'soft' : (125, 113, 76), 
        'soft blue' : (95, 105, 135)
}

speeds = {
        'fastest' : 10,
        'faster' : 5,
        'fast' : 3,
        'slow' : .3333,
        'slower' : .2,
        'slowest' : .1
}

if __name__ == "__main__":
    response = start(sys.argv[1:])[0]
    if not response is None:
        print response
    raw_input("Press any enter to stop...")
    stop_event.set()
    if t is not None:
        t.join()

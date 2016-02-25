import neopixels, socket, threading, time


t_stop = threading.Event()
t = None
def start():
    global t_stop
    global t
    # create a raw socket and bind it to the public interface
    si = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    #Allow socket to be reopened immediately after closing
    si.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #Binding to "" is the same as binding to any address
    si.bind(("", 42297))
    while True:    
        data, addr = si.recvfrom(1024) # buffer size is 1024 bytes
        #print data + " from " + str(addr[0]) + " : " + str(addr[1])
        if(not neopixels.is_effect(data)):
           ret = neopixels.help()
        else:
            #Setting the event makes the script halt
            t_stop.set()
            #Wait for the previous thread to stop
            if not t is None:
                t.join()
            #Reset the flag for the next thread
            t_stop.clear()
            #start the next
            ret, thread = neopixels.start(data.split(), t_stop)
            t = thread
        if not ret is None:
            print ret
            so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            so.sendto(ret, (addr[0], 42297))
            so.close()

if __name__=="__main__":
    start()
atexit.register(s.close)

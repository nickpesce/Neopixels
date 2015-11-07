import neopixels, socket, threading, time


def start(args, t_stop,  addr):
    error = neopixels.start(args, t_stop)
    if not error is None:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(error, addr)


t_stop = threading.Event()
t = None
# the public network interface
HOST = "nickspi.student.umd.edu"

# create a raw socket and bind it to the public interface
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
s.bind((HOST, 42297))
while True:    
    data, addr = s.recvfrom(1024) # buffer size is 1024 bytes
    #Setting the event makes the script halt
    t_stop.set()
    if not t is None:
       #Wait for the script to finish before continuing
        t.join()
    #Reset the flag for the next thread
    t_stop.clear()
    #Thread is needed for the script can run and this can listen for new commands at the same time
    t = threading.Thread(target=start, args=(data.split(), t_stop, addr))
    t.daemon = True
    t.start()

atexit.register(s.close)

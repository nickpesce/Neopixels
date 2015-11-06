import neopixels, socket, threading, time

global t

# the public network interface
HOST = "nickspi.student.umd.edu"

# create a raw socket and bind it to the public interface
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
s.bind((HOST, 42297))
while True:
    global t
    data, addr = s.recvfrom(1024) # buffer size is 1024 bytes
    neopixels.running = False
    t.join()
    t = threading.Thread(target=neopixels.start, args=(data.split(),))
    t.daemon = True
    t.start()
atexit.register(s.close)
import neopixels, socket, threading, time


t_stop = threading.Event()
t = None
def start():
    global t_stop
    global t
    # create a raw socket and bind it to the public interface
    si = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
    #Binding to "" is the same as binding to any address
    si.bind(("", 42297))
    #Start listening for TCP connections with a max backlog of 5
    si.listen(5);
    while True:    
        #Accept any connection.
        connect, addr = si.accept()
        data = connect.recv(1024) # buffer size is 1024 bytes
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
            #send the result back to the client.
            connect.send(ret);
        connect.close()
    si.close()

if __name__=="__main__":
    start()
atexit.register(s.close)

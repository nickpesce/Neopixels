import neopixels, socket, threading, time
import ConfigParser


t_stop = threading.Event()
t = None
config = ConfigParser.ConfigParser()
config.read("config.ini")
password = config.get("General", "password")
port = config.getint("General", "port")

def start():
    global t_stop
    global t
    # create a raw socket and bind it to the public interface
    si = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
    #Sets the socket to be able to be reused instantly after closing
    si.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #Binding to "" is the same as binding to any address
    si.bind(("", port))
    #Start listening for TCP connections with a max backlog of 5
    si.listen(5);
    while True:    
        #Accept any connection.
        connect, addr = si.accept()
        data = connect.recv(1024).split() # buffer size is 1024 bytes
        #print str(data) + " from " + str(addr[0]) + " : " + str(addr[1])
        #Check the password
        if(data[0] != password):
            ret = "Incorrect Password" 
        else:
            command = data[1:]
            if(not neopixels.is_effect(command[0])):
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
                ret, thread = neopixels.start(command, t_stop)
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

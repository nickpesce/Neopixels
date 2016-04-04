import neopixels, socket, threading, time
import ConfigParser

FLAG_RETURN = int('0b01', 2)
FLAG_STAY_CONNECTED = int('0b10', 2)

t_stop = threading.Event()
t = None
config = ConfigParser.ConfigParser()
config.read("config.ini")
password = config.get("General", "password")
port = config.getint("General", "port")
stack = []

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
        #Return string varaible
        ret = None
        #make a varaible for the flags. Set after effect is started.
        flags = 0;
        data = connect.recv(1024).split() # buffer size is 1024 bytes
        #print str(data) + " from " + str(addr[0]) + " : " + str(addr[1])
        #Ensure that there is a password and commands
        if(len(data) < 2):
            ret = "Not enough arguments"
        #Check the password
        elif(data[0] != password):
            ret = "Incorrect Password" 
        else:
            command = data[1:]
            if(command[0] == "revert" or command[0] == "last" or command[0] == "back"):
                if(len(stack) < 2):
                    ret = "There is no last effect!"
                else:
                    stack.pop()
                    command = stack.pop()
            if(not neopixels.is_effect(command[0])):
                if(ret == None):
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
                ret, f, thread, success = neopixels.start(command, t_stop)
                flags = f
                t = thread
                if(success):
                    stack.append(command);

        if not ret is None:
            print ret
            #send the result back to the client(unless -r flag is set).
            if(flags & FLAG_RETURN == 0):
                connect.send(ret)
        connect.close()
    si.close()

if __name__=="__main__":
    start()
atexit.register(s.close)

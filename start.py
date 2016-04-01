import socket, sys, ConfigParser

config = ConfigParser.ConfigParser()
config.read("config.ini")
TCP_IP = config.get("General", "hostname")
TCP_PORT = config.getint("General", "port")
password = config.get("General", "password")

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))
    sock.send(" ".join([password] + sys.argv[1:]))
    if('-r' not in sys.argv[1:]):
        try:
            #If the timeout is reached, an error will be thrown
            #and "No response" will be printed
            sock.settimeout(2)
            #Recv a packet from the server with a biffer of 1024 bytes
            resp = sock.recv(1024)
            #print the response to the terminal
            print resp
        except:
            print "No response"
except:
    #if there was an error establishing the socket connection.
    print "could not connect"
finally:
    #Always close the socket when done.
    sock.close()

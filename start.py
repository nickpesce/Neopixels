import socket, sys

UDP_IP = "nickspi.student.umd.edu"
UDP_PORT = 42297

try:
    socks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socks.sendto(" ".join(sys.argv[1:]), (UDP_IP, UDP_PORT))
except:
    print "could not connect"
    sys.exit(2)
finally:
    socks.close()

sockr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sockr.bind(("", UDP_PORT))
sockr.settimeout(2)
try:
    response, addr = sockr.recvfrom(1024)
    print response
except:
    print "no response"
finally:
    sockr.close()
import socket

UDP_IP = socket.gethostbyname("nickspi.student.umd.edu")
UDP_PORT = 42297
MESSAGE = "Hello, World!"
print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
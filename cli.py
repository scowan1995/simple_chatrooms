import socket
import sys
import time

host = "localhost"
port = 3001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
mystring = str(sys.argv[1])
s.sendall(mystring.encode("utf-8"))
print(str(s.recv(1024)))

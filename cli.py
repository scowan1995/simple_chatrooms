import socket
import sys

host = "localhost"
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
mystring = str(sys.argv[1])
s.sendall(mystring.encode("utf-8"))
while True:
  print(str(s.recv(1024)))
import socket
import sys
from threading import *

buffer_size = 8192

class Proxy2Server(Thread):
    def __init__(self, host, port):
        super(Proxy2Server, self).__init__()
        self.client = None # client socket not known yet
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))
    
    # run in thread
    def run(self):
        while True:
            data = self.server.recv(buffer_size)
            if data:
                print("[{}] <- {}".format(self.port, data))
                # forward to client
                self.client.sendall(data)

class Client2Proxy(Thread):

    def __init__(self, host, port):
        super(Client2Proxy, self).__init__()
        self.server = None # real server socket not known yet
        self.port = port
        self.host = host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # print("host : {}:{}".format(self.host, self.port))
        
        sock.bind((self.host, self.port))
        sock.listen(1)

        # waiting for connection
        self.client, addr = sock.accept()
    
    def run(self):
        while True:
            data = self.client.recv(buffer_size)
            if data:
                print("[{}] -> {}".format(self.port, data))
                # forward to server
                self.server.sendall(data)

class Proxy(Thread):

    def __init__(self, from_host, to_host, port):
        super(Proxy, self).__init__()
        self.from_host = from_host
        self.to_host = to_host
        self.port = port

        print("listen from {} and send to {} on port {}".format(self.from_host, self.to_host, self.port))
    
    def run(self):
        while True:
            print("[proxy({})] settings up".format(self.port))
            self.c2p = Client2Proxy(self.from_host, self.port) # waiting for a client
            self.p2s = Proxy2Server(self.to_host, self.port)

            print("[proxy({})] connection established".format(self.port))

            # link the client to server
            self.c2p.server = self.p2s.server
            self.p2s.client = self.c2p.client

            # start
            self.c2p.start()
            self.p2s.start()

try:
    listen_host = str(input("Enter an ip adress to listen : "))
    listen_port = int(input("Enter a port to listen : "))
    server = Proxy('0.0.0.0', listen_host,listen_port)
    server.start()
except KeyboardInterrupt:
    sys.exit(0)
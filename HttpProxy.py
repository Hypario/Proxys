import socket
import sys
from threading import *

config = {
    "HOST_NAME": "0.0.0.0",
    "BIND_PORT": 12345,
    "BUFFER_SIZE": 8192,
    "CONNECTION_TIMEOUT": 5,
    "MAX_CONNEXION": 10
}

class Proxy2Server(Thread):

    def __init__(self, conn):
        super(Proxy2Server, self).__init__()
        self.conn = conn # client conexion
    

    def run(self):
        # get the request from browser
        request = self.conn.recv(config["BUFFER_SIZE"])
        
        if request:
            request = request.decode('ISO-8859-1')
        
            # parse the first line
            first_line = request.split('\n')[0]

            # get url
            url = first_line.split(' ')[1]

            # find the webserver and port
            http_pos = url.find("://")          # find pos of ://
            if (http_pos==-1):
                temp = url
            else:
                temp = url[(http_pos+3):]       # get the rest of url

            port_pos = temp.find(":")           # find the port pos (if any)

            # find end of web server
            webserver_pos = temp.find("/")
            if webserver_pos == -1:
                webserver_pos = len(temp)

            webserver = ""
            to_port = -1
            if (port_pos==-1 or webserver_pos < port_pos):      # default port
                to_port = 80
                webserver = temp[:webserver_pos]
            else:       # specific port
                to_port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
                webserver = temp[:port_pos]

            print("Connect to: ", webserver, to_port)

            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((webserver, to_port))
                s.send(request.encode('ISO-8859-1')) # send request to webserver

                while 1:
                    # receive data from web server
                    data = s.recv(config["BUFFER_SIZE"])

                    if (len(data) > 0):
                        # send to browser
                        self.conn.send(data)
                    else:
                        break
                s.close()
                self.conn.close()
            except socket.error:
                if s:
                    s.close()
                if self.conn:
                    self.conn.close()
                sys.exit(1)
        

class Proxy(Thread):

    def __init__(self):
        super(Proxy, self).__init__()
        self.server = None #real server not known yet
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.sock.bind((config['HOST_NAME'], config['BIND_PORT']))

        self.host, self.port = self.sock.getsockname()
        print("Proxy listening on {}:{}".format(self.host, self.port))

        self.sock.listen(config["MAX_CONNEXION"])
    
    def run(self):
        while 1:
            # waiting for connection
            client, self.addr = self.sock.accept()

            server = Proxy2Server(client)
            server.start()

        self.sock.close()

proxy = Proxy()
proxy.start()

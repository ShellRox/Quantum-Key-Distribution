import socket
from threading import Thread
from qexceptions import qsocketerror

class public_channel(object):  # insecure public classical/quantum channel
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5005
        self.buffer_size = 1024  # can be minimized for efficiency
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reusable socket
        self.ip_list = []  # blacklist already created connections
        self.conn_list = []
        self.full_data = []

    def initiate_channel(self, *port):
        if len(port) > 0:
            self.port = str(port[0])

        try:
            self.socket.bind((self.host, self.port))
        except socket.error:
            raise qsocketerror("port {0} is occupied".format(self.port))

        self.socket.listen(1)

        print("initiated the channel on {0}:{1}, waiting for clients...".format(self.host, self.port))

        while True:
            conn, addr = self.socket.accept()  # initiate new serving thread for every new connection:
            if addr[0] not in self.ip_list:
                print("{0} has connected.".format(addr[0]))
                self.ip_list.append(addr[0])
                self.conn_list.append(conn)
                _thread = Thread(target=self.initiate_connection, args=(conn, addr))
                _thread.daemon = True
                _thread.start()
            else:
                print self.ip_list

    def initiate_connection(self, conn, addr):
        while True:
            data = conn.recv(self.buffer_size)
            if not data:
                break
            else:
                print("{0}: {1}".format(addr[0], data))
                for clients in self.conn_list:
                    clients.sendall(data)
        self.ip_list.remove(addr)
        conn.close()

from models import photon
import socket
from qexceptions import qsocketerror, qobjecterror
import ast

class sender(object):
    def __init__(self):
        self.photon_pulse_size = 170
        self.min_shared = 20
        self.photon_pulse = self.create_photon_pulse()
        self.buffer_size = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.basis = []
        self.other_basis = []

    def create_photon_pulse(self):
        photon_pulse = []
        for i in range(1, self.photon_pulse_size):
            photon_pulse.append(photon())
        return photon_pulse

    def send_photon_pulse(self, pulse):
        if not isinstance(pulse, list):
            raise qobjecterror("argument must be list")

        try:
            self.socket.send("qpulse:{0}".format(len(pulse)))
            self.socket.send("~"*len(pulse))
        except socket.error:
            raise qsocketerror("not connected to any channel")

    def listen_classical(self):
        try:
            print("listening to classical channel for basis...")
            while True:
                data = self.socket.recv(self.buffer_size)
                try:
                    literal = ast.literal_eval(data)
                except ValueError:
                    pass
                else:
                    if len(literal) > 0:
                        self.other_basis = literal
                        break
            self.socket.close()
        except socket.error:
            raise qsocketerror("not connected to any channel")

    def send_classical_bits(self, string):
        if not isinstance(string, str):
            raise qobjecterror("argument must be string")

        try:
            self.socket.send(string)
        except socket.error:
            raise qsocketerror("not connected to any channel")

    def connect_to_channel(self, address, port):
        try:
            self.socket.connect((address, port))
        except socket.error:
            raise qsocketerror("unable to connect")


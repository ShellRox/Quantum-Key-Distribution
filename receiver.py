from models import photon
import socket
from qexceptions import qsocketerror, qobjecterror
import ast

class receiver(object):
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer_size = 1024
        self.basis = []
        self.other_basis = []

    def listen_quantum(self):
        try:
            print("listening to quantum channel for photon pulse...")
            while True:
                data = self.socket.recv(self.buffer_size)
                pulse = data.split(":")
                if "qpulse" in data and len(pulse) == 2:
                    if str(pulse[1]).isdigit():
                        pulse_length = int(pulse[1])+1
                        self.basis = [p.basis for p in self.create_photon_pulse(pulse_length)]
                        break
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

    def create_photon_pulse(self, pulse_size):
        photon_pulse = []
        for i in range(1, pulse_size):
            photon_pulse.append(photon())
        return photon_pulse

    def connect_to_channel(self, address, port):
        try:
            self.socket.connect((address, port))
        except socket.error:
            raise qsocketerror("unable to connect")

from models import photon
import socket
from qexceptions import qsocketerror, qobjecterror
import ast

# TODO: make multithreaded classical receiver & sender

class receiver(object):
    def __init__(self):
        self.min_shared = 20  # safe option
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer_size = 1024
        self.basis = []
        self.other_basis = []
        self.shared_key = []
        self.sub_shared_key = []

    def listen_quantum(self):
        try:
            print("listening to quantum channel for photon pulse...")
            while True:
                data = self.socket.recv(self.buffer_size)
                pulse = data.split(":")
                if "qpulse" in data and len(pulse) == 2:
                    if str(pulse[1]).isdigit():
                        pulse_length = int(pulse[1])+1
                        self.basis = [p.polarization for p in self.create_photon_pulse(pulse_length)]
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

    def create_shared_key(self, basis, other_basis):
        if len(basis) != len(other_basis):
            raise qobjecterror("both pulses must contain the same amount of photons")
        else:
            i = 0
            while i != len(basis):
                if basis[i] == other_basis[i]:
                    if basis[i] == 0:
                        self.shared_key.append(0)
                    elif basis[i] == 90:
                        self.shared_key.append(1)
                    elif basis[i] == 45:
                        self.shared_key.append(0)
                    elif basis[i] == 135:
                        self.shared_key.append(1)
                i += 1

    def create_sub_shared_key(self, shared_key):
        self.sub_shared_key = shared_key[:(len(shared_key)//2)]

    def verify(self):
        if len(self.shared_key) == 0 or len(self.sub_shared_key) == 0:
            raise qobjecterror("key is not defined")
        else:
            pass

    def connect_to_channel(self, address, port):
        try:
            self.socket.connect((address, port))
        except socket.error:
            raise qsocketerror("unable to connect")

    def reset_socket(self):
        self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

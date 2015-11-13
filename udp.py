import socket
from configuration import Configuration as conf

class UDP:
    def __init__(self, timeout=5):
        self.timeout = timeout
        self.ports = conf.PORTS

    def send(self, UDP_IP, type , msg):
        sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        sock.sendto(msg, (UDP_IP, self.ports[type]))

    def recv(self, UDP_IP, type):
        sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        try:
            sock.bind((UDP_IP, self.ports[type]))
            sock.settimeout(self.timeout)
            data,addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        except socket.error:
            data = None
            addr = None
        return data,addr

def test():
    #ports = {"prepare":12345, "promise":12346, "accept":12347, "ack":12348, "commit":12349}
    udp = UDP()
    msg = {"slot":0,"accNum":1, "accVal":"val"}
    udp.send("localhost", "promise", str(msg))
    udp.send("localhost", "ack", str(msg))

#udp.recv("localhost")

#test()
import threading
import socket
import time

def UDPClient():
    print threading.currentThread().getName(), 'Starting'
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005
    MESSAGE = "Hello, World!"

    print "UDP target IP:", UDP_IP
    print "UDP target port:", UDP_PORT
    print "UDP sending message:", MESSAGE
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    print threading.currentThread().getName(), 'Exiting'
    return

def UDPServer():
    print threading.currentThread().getName(), 'Starting'
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(20) # buffer size is 1024 bytes
        print "UDP received message:", data
    print threading.currentThread().getName(), 'Exiting'
    return

def TCPClient():
    print threading.currentThread().getName(), 'Starting'
    TCP_IP = '127.0.0.1'
    TCP_PORT = 12345
    BUFFER_SIZE = 1024
    MESSAGE = "Hello, World!"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE)
    s.close()

    print "TCP client received data:", data
    print threading.currentThread().getName(), 'Exiting'
    return

def TCPServer():
    print threading.currentThread().getName(), 'Starting'
    TCP_IP = '127.0.0.1'
    TCP_PORT = 12345
    BUFFER_SIZE = 20  # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    print 'TCP Connection address:', addr
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        print "TCP Server received data:", data
        conn.send(data)  # echo
    conn.close()
    print threading.currentThread().getName(), 'Exiting'
    return

tUDPServer = threading.Thread(target=UDPServer)
tUDPServer.daemon = True
tUDPServer.start()

time.sleep(1)

tUDPClient = threading.Thread(target=UDPClient)
tUDPClient.daemon = True
tUDPClient.start()

time.sleep(1)

tTCPServer = threading.Thread(target=TCPServer)
tTCPServer.daemon = True
tTCPServer.start()

time.sleep(1)

tTCPClient = threading.Thread(target=TCPClient)
tTCPClient.daemon = True
tTCPClient.start()

while threading.active_count() > 0:
    time.sleep(0.1)

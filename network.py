import threading
import sys
import select
import socket
import time
from configuration import Configuration

#tag:print
def printdata(head, node, source, end, data):
    print "P%d: %s %d-->%d data=[%s]" %( node, head, source, end, data)

#tag:udpclient
def UDPClient():
    ID = Configuration.getMyID()
    print threading.currentThread().getName(), 'UDP Client Starting. I am Node#', ID
  
    for ip in Configuration.IPTABLE:
        UDP_IP = ip
        UDP_PORT = Configuration.UDPPORT 
        MESSAGE = "Hello, World! from node %d" % ID 

        #print "UDP target IP:", UDP_IP
        #print "UDP target port:", UDP_PORT
        #print "UDP sending message:", MESSAGE
        printdata("UDP Send ", ID, ID, Configuration.getID( UDP_IP ) , MESSAGE )
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    print threading.currentThread().getName(), 'UDP Client Exiting. I am Node#', ID
    return

#tag:udpserver
def UDPServer():
    ID = Configuration.getMyID()
    print threading.currentThread().getName(), 'UDP Server Starting. I am Node#', ID
    UDP_PORT = Configuration.UDPPORT 

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind(('', UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        printdata("UDP Recv", ID, Configuration.getID( addr[0] ) , ID, data )
    print threading.currentThread().getName(), 'UDP Server Exiting. I am Node#', ID
    return

#tag:tcpclient
def TCPClient():
    MYIP = Configuration.getPublicIP()
    ID = Configuration.getMyID()
    print threading.currentThread().getName(), 'TCP Client Starting. I am Node#', ID

    for ip in Configuration.IPTABLE:
        if ip == MYIP: continue #Ignore itself
        TCP_IP = ip 
        TCP_PORT = Configuration.TCPPORT 
        BUFFER_SIZE = 1024
        MESSAGE = "Hello, World! from Node#%d" % ID
    
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        flag = True
        while flag:
            try:
                s.connect((TCP_IP, TCP_PORT))
                s.send(MESSAGE)
                printdata("TCP Send", ID, ID, Configuration.getID(TCP_IP), MESSAGE)
                data = s.recv(BUFFER_SIZE)
                s.close()
                flag = False
            except:
                printdata("TCP Reconnect", ID, ID, Configuration.getID(TCP_IP), "@_@")
                time.sleep(1) #Reconnect delay 
    
    print threading.currentThread().getName(), 'TCP Client Exiting. I am Node #', ID
    return

#tag:tcpserver
def TCPServer():
    ID = Configuration.getMyID()
    MYIP = Configuration.getPublicIP()
    print threading.currentThread().getName(), 'TCP Server Starting. I am Node#', ID, "ip=", MYIP
    TCP_PORT = Configuration.TCPPORT 
    BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(( socket.gethostname(), TCP_PORT))
    server.listen(5) #At most 5 concurrent connection
    input = [server, sys.stdin] 
    running = 1 
    while running: 
        inputready,outputready,exceptready = select.select(input,[],[]) 
    
        for s in inputready: 
            if s == server: 
                # handle the server socket 
                client, address = server.accept() 
                print 'NODE#', ID,'<-----connect-----> NODE#' , Configuration.getID(address[0])
                input.append(client) 
    
            elif s == sys.stdin: 
                # handle standard input 
                junk = sys.stdin.readline() 
                running = 0 
    
            else: 
                # handle all other sockets 
                data = s.recv(BUFFER_SIZE) 
                print "PEERNAME", s.getpeername()
                #printdata("TCP Recv", ID, Configuration.getID(addr[0]), ID, data)
                if data: 
                    s.send(data) 
                else: 
                    print "LOST CONNECTION FROM ", s.getpeername()
                    s.close() 
                    input.remove(s) 
    server.close()

    print threading.currentThread().getName(), 'TCP Server Exiting. I am NODE#', ID
    return

#tUDPServer = threading.Thread(target=UDPServer)
#tUDPServer.daemon = True
#tUDPServer.start()
#
#time.sleep(5)
#
#tUDPClient = threading.Thread(target=UDPClient)
#tUDPClient.daemon = True
#tUDPClient.start()
#
#time.sleep(1)

tTCPServer = threading.Thread(target=TCPServer)
tTCPServer.daemon = True
tTCPServer.start()

time.sleep(5)

tTCPClient = threading.Thread(target=TCPClient)
tTCPClient.daemon = True
tTCPClient.start()

while threading.active_count() > 0:
    time.sleep(0.1)

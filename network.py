import threading
import pdb
import sys
import select
import socket
import time
from configuration import Configuration

#tag:print
def printdata(head, node, source, end, data):
    print "NODE#%d: %s %d=====>%d data=[%s]" %( node, head, source, end, data)

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

def TCPSend(dest, content):
    TCP_IP = Configuration.getIP(dest) 
    MYIP = Configuration.getPublicIP()
    if TCP_IP == MYIP:
       print "TCPSend() terminates. (Error: sending to itself)" #Ignore itself
       return
    TCP_PORT = Configuration.TCPPORT 
    ID = Configuration.getMyID()
    print threading.currentThread().getName(), 'TCP Client Starting. I am Node#', ID
    BUFFER_SIZE = 1024
    MESSAGE = "Hello, World! from Node#%d" % ID
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    flag = True
    while flag:
        try:
            s.connect((TCP_IP, TCP_PORT))
            s.send(content)
            printdata("TCP Send", ID, ID, Configuration.getID(TCP_IP), content)
            data = s.recv(BUFFER_SIZE)
            s.close()
            flag = False
        except:
            printdata("TCP Client Reconnect", ID, ID, Configuration.getID(TCP_IP), "@_@")
            time.sleep(1) #Reconnect delay 
    time.sleep(5)
    
    print threading.currentThread().getName(), 'TCP Client Exiting Successfully. I am Node #', ID
    return 

#tag:tcpclient
def TCPClient():
    MYIP = Configuration.getPublicIP()
    ID = Configuration.getMyID()
    print threading.currentThread().getName(), 'TCP Client Starting. I am Node#', ID

    while True:
        user_input = raw_input("format: send <Dest Node ID> <Message>")
        cmd = user_input.split(" ")
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
                    printdata("TCP Client Reconnect", ID, ID, Configuration.getID(TCP_IP), "@_@")
                    time.sleep(1) #Reconnect delay 
        time.sleep(5)
    
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
    input = [server] 
    running = 1 
    while running: 
        inputready,outputready,exceptready = select.select(input,[],[]) 
    
        for s in inputready: 
            if s == server: 
                # handle the server socket 
                client, address = server.accept() 
                input.append(client) 
                print 'TCP Server NODE#', ID,'<-----connect-----> NODE#' , Configuration.getID(address[0]) , "TCP Client (", len(input) - 2, "over", Configuration.getN() - 1, "connections)"
    
            else: 
                # handle all other sockets 
                data = s.recv(BUFFER_SIZE) 
                printdata("TCP Recv", ID, Configuration.getID(s.getpeername()[0]), ID, data)
                if data: 
                    s.send(data) 
                else: 
                    print "LOST CONNECTION FROM NODE#%d :  %s" %(Configuration.getID(s.getpeername()[0]), s.getpeername())
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

#tTCPClient = threading.Thread(target=TCPClient)
#tTCPClient.daemon = True
#tTCPClient.start()

TCPSend(1, "Love")
TCPSend(2, "Faith")
TCPSend(1, "Hope")
TCPSend(2, "Love is the most important")

while threading.active_count() > 0:
    time.sleep(0.1)

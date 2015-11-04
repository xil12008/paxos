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
            time.sleep(2) #Reconnect delay 
    print threading.currentThread().getName(), 'TCP Client Exiting Successfully. I am Node #', ID
    return 

#tag:tcpserver
def TCPServer():
    ID = Configuration.getMyID()
    N = Configuration.getN()
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
            else: 
                # handle all other sockets 
                data = s.recv(BUFFER_SIZE) 
                printdata("TCP Recv", ID, Configuration.getID(s.getpeername()[0]), ID, data)
                if data: 
                    #s.send(data) 
                    #forward to the next node
                    TCPSend( ID % N + 1, data )
                else: 
                    s.close() 
                    input.remove(s) 
    server.close()

    print threading.currentThread().getName(), 'TCP Server Exiting. I am NODE#', ID
    return

tTCPServer = threading.Thread(target=TCPServer)
tTCPServer.daemon = True
tTCPServer.start()

time.sleep(5)

TCPSend(2, "Faith")

while threading.active_count() > 0:
    time.sleep(0.1)

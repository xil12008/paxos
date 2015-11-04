from threading import Timer
import threading
import pdb
import sys
import select
import socket
import time
from configuration import Configuration

winFlag = True #Default is that a process will thought it is the highest-ID alive process

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
    #print threading.currentThread().getName(), 'TCP Client Starting. I am Node#', ID
    BUFFER_SIZE = 1024
    count = 0;
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    flag = True
    while flag and count < 5:
        try:
            s.connect((TCP_IP, TCP_PORT))
            s.send(content)
            printdata("TCP Send", ID, ID, Configuration.getID(TCP_IP), content)
            #data = s.recv(BUFFER_SIZE)
            s.close()
            flag = False
        except:
            printdata("TCP Client Reconnect", ID, ID, Configuration.getID(TCP_IP), "@_@_~:" + content)
            time.sleep(2) #Reconnect delay 
            count += 1
    #print threading.currentThread().getName(), 'TCP Client Exiting Successfully. I am Node #', ID
    return 

def bcastCoordinator():
    global winFlag
    if winFlag == False: return
    for i in range(1, Configuration.getN() + 1):
        TCPSend(i, "Coordinator")

def holdElection(ID):
    for bi in range(ID + 1, Configuration.getN() + 1):
        TCPSend( bi, "ELECTION") 
    global winFlag
    winFlag = True 
    t = Timer(20.0, bcastCoordinator)
    t.start()

#tag:tcpserver
def TCPServer():
    ID = Configuration.getMyID()
    N = Configuration.getN()
    MYIP = Configuration.getPublicIP()
    print threading.currentThread().getName(), 'TCP Server Starting. I am Node#', ID, "ip=", MYIP
    TCP_PORT = Configuration.TCPPORT 
    BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

    _state_ = "NULL"

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
                if data: 
                    peerID =  Configuration.getID( s.getpeername()[0] )
                    printdata("TCP Recv", ID, peerID, ID, data)
                    #s.send(data) 
                    #forward to the next node
                    time.sleep(1)
                    if data[0] == 'C': #Coordinate
                        print "NODE #", ID, "Leader is", peerID
                    elif data[0] == 'E': #Election
                        if peerID < ID:
                            TCPSend( peerID, "OK" )
                            holdElection(ID)
                    elif data[0] == 'O': #OK
                        print "NODE #", ID, "Gave up. (Receive OK from", peerID, ")"
                        global winFlag
                        winFlag = False
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

userinput = raw_input("Press A to hold election...")
if userinput == "A":
  print "hold election now"
  ID = Configuration.getMyID()
  holdElection(ID)

while threading.active_count() > 0:
    time.sleep(0.1)
import threading
import pdb
import json
import sys
import select
import socket
import time
import pickle
from configuration import Configuration

#tag:print
def printdata(head, node, source, end, data):
    print "NODE#%d: %s %d=====>%d data=[%s]" %( node, head, source, end, data)

#tag:udpserver
def acceptor_udp_server():
    ID = Configuration.getMyID()
    UDP_PORT = Configuration.ACCEPTOR_PORT
    print threading.currentThread().getName(), ' Acceptor UDP Server Starting. I am Node#', ID, "at port", UDP_PORT

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind(('', UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        peerID = Configuration.getID( addr[0] )
        printdata("Acceptor UDP Recv", ID, peerID, ID, data)
        try:
            pdb.set_trace()
            json_object = json.loads(data.strip())
            if json_object['msgname'] == "commit": 
               onCommit(json_object['entryID'], json_object['msglist']) 
        except:
            print "Can't parse data:", data
    print threading.currentThread().getName(), ' Acceptor UDP Server Exiting. I am Node#', ID
    return

def onPrepare():
    pass

def onAccept():
    pass

def onCommit(entryID, msglist):
    locallog = pickle.load( open( "locallog.p", "rb" ) )
    locallog[entryID] = msglist[0]
    pickle.dump( favorite_color, open( "locallog.p", "wb" ) )

def udp_send(): 
    ID = Configuration.getMyID()
    UDP_IP = Configuration.getPublicIP() 
    UDP_PORT = Configuration.ACCEPTOR_PORT
    msg = {}
    msg['msgname'] = "commit"
    msg['entryID'] = 10 
    msg['msglist'] = ["test value"]
    MESSAGE = json.dumps(msg) 
    printdata("UDP Send ", ID, ID, Configuration.getID( UDP_IP ) , MESSAGE )
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


tAcceptor = threading.Thread(target=acceptor_udp_server)
tAcceptor.daemon = True
tAcceptor.start()

time.sleep(5)

udp_send()

while threading.active_count() > 0:
    time.sleep(0.1)


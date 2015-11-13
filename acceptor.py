import threading
import ast
import pdb
import json
import sys
import select
import socket
import time
import csv
from configuration import Configuration

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#tag:print
def printdata(head, node, source, end, data):
    print bcolors.OKBLUE + "NODE#%d: %s %d=====>%d data=[%s]" %( node, head, source, end, data) + bcolors.ENDC

#tag:udpserver
def acceptor_udp_server():
    ID = Configuration.getMyID()
    #UDP_PORT = Configuration.ACCEPTOR_PORT
    UDP_PORT = Configuration.PORTS["prepare"]
    print threading.currentThread().getName(), ' Acceptor UDP Server Starting. I am Node#', ID, "at port", UDP_PORT

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind(('', UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        peerID = Configuration.getID( addr[0] )
        #try:
        json_object = json.loads(data.strip())
        if json_object['msgname'] == "commit": 
           onCommit(json_object['entryID'], json_object['msglist'], peerID) 
           printdata("Acceptor Recv Commit", ID, peerID, ID, data)
        elif json_object['msgname'] == "accept":
           onAccept(json_object['entryID'], json_object['msglist'], peerID) 
           printdata("Acceptor Recv Accept", ID, peerID, ID, data)
        elif json_object['msgname'] == "prepare":
           onPrepare(json_object['entryID'], json_object['msglist'], peerID) 
           printdata("Acceptor Recv Prepare", ID, peerID, ID, data)
        #except:
        #    print "Can't parse data:", data, sys.exc_info()[0]
    print threading.currentThread().getName(), ' Acceptor UDP Server Exiting. I am Node#', ID
    return

def firstRun():
    locallog = readlog() 
    if not locallog: 
        for i in range( 0, 10): 
            if i not in locallog:
                locallog[i] = {'maxPrepare': Configuration.init_maxPrepare,\
                               'accNum': Configuration.init_accNum,\
                               'accVal': Configuration.init_accVal,\
                               'value' : Configuration.init_value }
    savelog(locallog)

def onPrepare(entryID, msglist, peerID):
    print bcolors.BOLD + "onPrepare:" + bcolors.ENDC + " entryID=", entryID, ", m=", msglist, "from NODE", peerID
    m = int(msglist[0])
    entryID = str(entryID)
    locallog = readlog()
    if ( m > int(locallog[entryID]["maxPrepare"]) ):
        locallog[entryID]["maxPrepare"] = m
        send_msglist = [locallog[entryID]["accNum"], locallog[entryID]["accVal"]]
        print bcolors.WARNING + "send promise" + bcolors.ENDC
        udp_send(entryID, "promise", send_msglist, peerID) 
    else:
        print bcolors.FAIL + "rejected" + bcolors.ENDC
    savelog(locallog)

def onAccept(entryID, msglist, peerID):
    print bcolors.BOLD + "onAccept:" + bcolors.ENDC + " entryID=", entryID, ", m:v=", msglist, " from NODE", peerID
    m = int(msglist[0])
    entryID = str(entryID)
    v = msglist[1]
    locallog = readlog()
    if ( m >= int(locallog[entryID]['maxPrepare']) ):
        locallog[entryID]['accNum'] = m
        locallog[entryID]['accVal'] = v 
        send_msglist = [locallog[entryID]['accNum'], locallog[entryID]['accVal']]
        print bcolors.WARNING + "send ack" + bcolors.ENDC
        udp_send(entryID, "ack", send_msglist, peerID) 
    else:
        print bcolors.FAIL + "rejected" + bcolors.ENDC
    savelog(locallog)

def onCommit(entryID, msglist, peerID):
    print bcolors.BOLD + "onCommit:" + bcolors.ENDC + " entryID=", entryID, ", v=", msglist, "from NODE", peerID
    locallog = readlog()
    locallog[entryID]["value"] = msglist[0]
    savelog(locallog)

def udp_send(entryID, msgname, msglist, peerID): 
    ID = Configuration.getMyID()
    UDP_IP = Configuration.getIP(peerID) 
    UDP_PORT = Configuration.PORTS[msgname]
    msg = {}
    msg['msgname'] = msgname 
    msg['entryID'] = str( entryID ) 
    msg['msglist'] = msglist 
    MESSAGE = json.dumps(msg) 
    printdata("UDP Send" + msgname, ID, ID, Configuration.getID( UDP_IP ) , MESSAGE )
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

def savelog(dict):
    w = csv.writer(open("log.csv", "w+"))
    for key, val in dict.items():
        w.writerow([key, val])

def readlog():
    dict = {}
    try:
        for key, val in csv.reader(open("log.csv")):
            dict[key] = ast.literal_eval(val)
    finally:
        return dict

firstRun()

tAcceptor = threading.Thread(target=acceptor_udp_server)
tAcceptor.daemon = True
tAcceptor.start()

time.sleep(2)

#udp_send( 1, "commit", ["value hahaha"] ) 
#udp_send( 1, "commit", ["value hahaha"], Configuration.getMyID() ) 
udp_send( 3, "prepare", ["4"] , Configuration.getMyID()) 
udp_send( 3, "prepare", ["2"] , Configuration.getMyID()) 
udp_send( 3, "prepare", ["5"] , Configuration.getMyID()) 
#udp_send( 3, "prepare", ["2"] ) 
udp_send( 3, "accept", ["5", "my test value"] , Configuration.getMyID()) 
udp_send( 3, "commit", ["my test value"] , Configuration.getMyID()) 

while threading.active_count() > 0:
    time.sleep(0.1)


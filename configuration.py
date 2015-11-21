#!/bin/python
from urllib2 import urlopen

'''
   This file is for configuration
'''

class Configuration:
    IPTABLE = ['52.33.142.238','54.183.195.158','52.1.87.58','52.18.239.201','54.94.201.162']
    #IPTABLE = ['52.1.87.58','52.18.239.201','54.94.201.162']
    #IPTABLE = ['localhost']
    UDPPORT = 5005 #UDP PORT
    TCPPORT = 12345 #TCP PORT
    PORTS = {"prepare":12345, "promise":12346, "maxPrepare":12346, "accept":12345, "ack":12348, "commit":12345, "request":12345, "update":12347}
    
    ACCEPTOR_PORT = 12346
    LEADER_PORT = 12347
    BULLY_PORT = 5005
    
    init_accNum = -99999
    init_accVal = -99999
    init_maxPrepare = -99999
    init_value = "Nothing"
  
    @staticmethod
    def getN():
        return len(Configuration.IPTABLE)

    @staticmethod 
    def getPublicIP():
        return urlopen('http://ip.42.pl/raw').read()

    @staticmethod 
    def getMyID():
        return Configuration.getID(urlopen('http://ip.42.pl/raw').read())
    
    @staticmethod 
    def getID(ip):
        for index, ele in enumerate(Configuration.IPTABLE):
            if ele==ip:
                return index + 1
    
    @staticmethod 
    def getIP(nodeID):
        nodeID -= 1
        if(nodeID >= len(Configuration.IPTABLE)): 
            print "Sorry, nodeID too large"
            return None
        return Configuration.IPTABLE[nodeID]

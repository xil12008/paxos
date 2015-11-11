#!/bin/python
from urllib2 import urlopen

'''
   This file is for configuration
'''

class Configuration:
    IPTABLE = ['52.32.80.147','54.175.20.156','52.23.155.239', '54.193.79.49']
    UDPPORT = 5005 #UDP PORT
    TCPPORT = 12345 #TCP PORT
    
    ACCEPTOR_PORT = 12346
    LEADER_PORT = 12347
    BULLY_PORT = 5005
    
    init_accNum = -99999
    init_accVal = -99999
  
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

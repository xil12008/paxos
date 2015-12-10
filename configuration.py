#!/bin/python
from urllib2 import urlopen

'''
   This file is for configuration
'''

class Configuration:
    IPTABLE = [ '52.76.168.152', '52.18.239.201', '54.94.201.162', '52.34.51.172', '54.193.52.50']
    #IPTABLE = [ '52.33.193.176', '52.35.88.44', '52.53.219.123', '52.23.248.210', '52.90.150.45' ]
    #UDPPORT = 5005 #UDP PORT
    TCPPORT = 13333 #TCP PORT
    PORTS = {"prepare":12345, "promise":12346, "maxPrepare":12346, "accept":12345, "ack":12348, "commit":12345, "event":12350, "complete":12351}
    
    init_accNum = -99999
    init_accVal = -99999
    init_maxPrepare = -99999
    init_value = "Nothing"

    leader = -1
  
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

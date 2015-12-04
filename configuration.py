#!/bin/python
from urllib2 import urlopen

'''
   This file is for configuration
'''

class Configuration:
    IPTABLE = ['128.213.11.178', '129.161.71.169', '52.24.19.40', '52.33.213.92']
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

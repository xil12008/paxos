#!/bin/python
from urllib2 import urlopen

'''
   This file is for configuration
'''

class Configuration:
    IPTABLE = ['52.32.80.147','52.33.9.72','52.23.155.239', '54.193.79.49']
    UDPPORT = 5005 #UDP PORT
    TCPPORT = 12345 #TCP PORT
  
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

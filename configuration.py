#!/bin/python
from urllib2 import urlopen

'''
   This file is for configuration
'''

class Configuration:
    IPTABLE = ['52.32.150.64','52.32.71.203']
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
        if(nodeID >= len(Configuration.IP_Table)): 
            print "Sorry, nodeID too large"
            return None
        return Configuration.IPTABLE[nodeID]

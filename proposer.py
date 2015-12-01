import random
import udp
from synod import Synod
from threading import Thread
from configuration import Configuration

class Proposer(Thread):
    def __init__(self, opt):
        Thread.__init__(self)
        self.opt = opt
        self.UDP = udp.UDP()
        self.synods = {}
        self.ID = Configuration.getMyID()
        print "opt"+str(self.opt)

    def getSynod(self, entryID, event=None):
        if entryID not in self.synods:
            self.synods[entryID]=Synod(self.opt, entryID, event)
        self.synods[entryID].setEvent(event)
        return self.synods[entryID]

    def eventCheck(self, entryID):
        synod = self.getSynod(entryID)
        synod.phase1()
        return synod.v!=None

    # st1 start_time_1 et2 end_time_2
    def timeConflict(self, st1, et1, st2, et2):
        return (st1<et2 and st2<et1)

    def hasConflict(self, event):
        for entryID in self.synods:
            synod = self.synods[entryID]
            if synod.v == None: continue
            if synod.v["app_name"] == event["app_name"] : return True
            if self.timeConflict(synod.v["startTime"],synod.v["endTime"],event["startTime"],event["endTime"]) : return True
        return False

    def noEventDel(self, event):
        for entryID in self.synods:
            synod = self.synods[entryID]
            if synod.v == None: continue
            if synod.v["app_name"] == event["app_name"] : return False
        return True

    def paxos(self, event):
        entryID = 0
        while(True):
            entryID+=1
            if self.synods.has_key(entryID) : continue
            if self.eventCheck(entryID) :
                synod = self.getSynod(entryID)
                synod.allPhases()
            else :
                if event["operation"]=="add" and self.hasConflict(event):
                    print "conflict", event
                    break
                elif event["operation"]=="del" and self.noEventDel(event):
                    print "no delete", event
                    break
                synod = self.getSynod(entryID, event)
                synod.allPhases()
                break

    def run(self):
        while self.ID == Configuration.leader:
            data,addr = self.UDP.recv('', "event")
            if data == None : continue
            user = addr[0]
            event = eval(data)
            self.paxos(event)
            self.UDP.send(user,"complete","finish event")
        print "proposer(leader) quit"


def testPaxos():
    proposer = Proposer(random.randint(0,1)==0)
    proposer.run()

#testPaxos()

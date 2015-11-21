import random
from synod import Synod

class Proposer:
    def __init__(self, opt):
        self.opt = opt
        self.values = {}
        self.synods = {}
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
            if entryID in self.values : continue
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

def getTime():
    startTime = 0
    endTime = 0
    while(startTime>=endTime):
        startTime = random.randint(0,10)
        endTime = random.randint(0,10)
    return startTime, endTime

def testPaxos():
    proposer = Proposer(random.randint(0,1)==0)
    startTime, endTime = getTime()
    proposer.paxos({"operation":"add", "app_name":random.randint(0,1), "startTime":startTime, "endTime":endTime})

testPaxos()
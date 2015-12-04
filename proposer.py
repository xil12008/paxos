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

    def constructCalendar(self):
        self.calendar={}
        for entryID in self.synods:
            entryVal = self.synods[entryID].v
            if entryVal==None: continue
            if entryVal["operation"] == "add":
                if entryVal["app_name"] in self.calendar.keys():
                    print "Error: add same appointment name for mulitiple times."
                    break
                self.calendar[entryVal["app_name"]] = entryVal
            elif entryVal["operation"] == "del":
                if not entryVal["app_name"] in self.calendar.keys():
                    print "Error: try to delete an non-exist appointment."
                    break
                self.calendar.pop(entryVal["app_name"], None)

    def readLog(self):
        record = {}
        try:
            f = open('acceptor.state', 'r')
            for line in f: record = eval(line)
        except: ""
        for entryID in record.keys():
            if self.synods.has_key(entryID): continue
            if "maxPrepare" not in record[entryID].keys(): continue
            if "commitVal" not in record[entryID].keys(): continue
            self.getSynod(entryID)
            self.synods[entryID].m = record[entryID]["maxPrepare"]
            self.synods[entryID].v = record[entryID]["commitVal"]

    # st1 start_time_1 et2 end_time_2
    def timeConflict(self, st1, et1, st2, et2):
        return (st1<et2 and st2<et1)

    def hasConflict(self, event):
        for app_name in self.calendar:
            if app_name == event["app_name"] : return True
            app = self.calendar[app_name]
            if app == None: continue
            if app["day"]!=event["day"] : continue
            if app["participants"].isdisjoint(event["participants"]) : continue
            if self.timeConflict(app["startTime"],app["endTime"],event["startTime"],event["endTime"]) : return True
        return False

    def noEventDel(self, event):
        return not self.calendar.has_key(event["app_name"])

    def paxos(self, event):
        entryID = 0
        self.readLog()
        while(True):
            entryID+=1
            if self.synods.has_key(entryID) and self.synods[entryID].v!=None : continue
            if self.eventCheck(entryID) :
                synod = self.getSynod(entryID)
                synod.allPhases()
            else :
                self.constructCalendar()
                if event["operation"]=="add" and self.hasConflict(event):
                    print "\033[91m<=================|==o"
                    print "conflict", event
                    print "o===|================>\033[0m"
                    break
                elif event["operation"]=="del" and self.noEventDel(event):
                    print "\033[91m<=================|==o"
                    print "no delete", event
                    print "o===|================>\033[0m"
                    break
                elif event["operation"]=="view": break

                synod = self.getSynod(entryID, event)
                synod.allPhases()
                break

    def run(self):
        print "^_^ I am the leader(proposer) now. ^_^"
        while self.ID == Configuration.leader:
            data,addr = self.UDP.recv('', "event")
            if data == None : continue
            user = addr[0]
            event = eval(data)
            self.paxos(event)
            if event["operation"]!="view":
                self.UDP.send(user,"complete","finish event")
            else:
                self.UDP.send(user,"complete",str(self.calendar))
        print "$_$ proposer(leader) quit $_$"


def testPaxos():
    proposer = Proposer(random.randint(0,1)==0)
    proposer.run()

#testPaxos()

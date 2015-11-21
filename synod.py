import udp
from configuration import Configuration as conf

class Synod:
    def __init__(self, opt, entryID, value):
        self.acceptors_ip = conf.IPTABLE
        self.UDP = udp.UDP()
        self.acceptors_num = len(self.acceptors_ip)
        self.entryID = entryID
        self.m = self.getMaxPrepare()
        self.v = value
        self.opt = opt
        print "opt"+str(self.opt)

    def setEvent(self, event):
        self.v = event

    def getMaxPrepare(self):
        maxPrepare = 0
        return maxPrepare

    def prepare(self):
        msg = {"entryID":self.entryID, "msgname":"prepare", "id":self.m}
        for acceptor_ip in self.acceptors_ip:
            self.UDP.send(acceptor_ip, msg["msgname"], str(msg))

    def select_val(self, majority):
        highest_num=0
        val = self.v
        for msg in majority:
            if msg["accNum"]<self.m and msg["accNum"]>highest_num:
                highest_num = msg["accNum"]
                val = msg["accVal"]
        self.v = val

    def translateMsg(self, data):
        msg = eval(data)
        return msg

    def promise(self):
        majority = []
        for acceptor_ip in self.acceptors_ip:
            data,addr = self.UDP.recv('', "promise")
            if data == None: continue
            msg = self.translateMsg(data)
            if msg["msgname"] == "maxPrepare":
                self.m = msg["maxPrepare"]
            elif msg["msgname"] == "promise":
                if msg["accNum"] >= self.m : continue
                majority.append(msg)
        print "promise majority:", majority
        if len(majority)<=self.acceptors_num/2:
            return False
        else :
            self.select_val(majority)
            return True

    def accept(self):
        msg = {"entryID":self.entryID, "msgname":"accept", "id":self.m, "val":self.v}
        for acceptor_ip in self.acceptors_ip:
            self.UDP.send(acceptor_ip, msg["msgname"], str(msg))

    def ack(self):
        majority = []
        for acceptor_ip in self.acceptors_ip:
            data,addr = self.UDP.recv('', "ack")
            if data == None: continue
            msg = self.translateMsg(data)
            if msg["msgname"] != "ack": continue
            if msg["accNum"] != self.m : continue
            if msg["accVal"] != self.v : continue
            majority.append(msg)
        print "ack majority:", majority
        if len(majority)<=self.acceptors_num/2 : return False
        else : return True

    def commit(self):
        msg = {"entryID":self.entryID, "msgname":"commit", "id":self.m, "val":self.v}
        for acceptor_ip in self.acceptors_ip:
            self.UDP.send(acceptor_ip, msg["msgname"], str(msg))

    def phase1(self):
        self.m +=1
        self.prepare()
        promise = self.promise()
        print "promise:\t"+str(promise)
        if not promise : self.phase1()


    def phase2(self):
        self.accept()
        ack = self.ack()
        print "ack:\t"+str(ack)
        if ack : self.commit()
        else :
            if self.opt : self.phase2()
            else : self.allPhases()


    def allPhases(self):
        self.phase1()
        self.phase2()
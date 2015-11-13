import random
import udp
from configuration import Configuration as conf

class Proposer:
    def __init__(self, opt):
        self.acceptors_ip = conf.IPTABLE
        self.UDP = udp.UDP()
        self.acceptors_num = len(self.acceptors_ip)
        self.entryID = self.getEntryID()
        self.m = self.getMaxPrepare()
        self.v = self.getValue()
        self.opt = opt
        print "opt"+str(self.opt)
    
    def getMaxPrepare(self):
        '''
        while(True):
            maxPrepare = 0
            count = 0
            for acceptor_ip in self.acceptors_ip:
                send_msg = {"msgname":"request", "entryID":self.entryID}
                self.UDP.send(acceptor_ip, send_msg["msgname"], str(send_msg))
                data = self.UDP.recv(acceptor_ip, "update")
                if data == None: break
                recv_msg = eval(data)
                if recv_msg["msgname"]!="update": break
                maxPrepare = max(maxPrepare, recv_msg["maxPrepare"])
                count += 1
            if count==self.acceptors_num: break
        '''
        maxPrepare = 0
        return maxPrepare
    
    def getValue(self):
        return "dummy" #toDo
    
    def getEntryID(self):
        return 0 #toDo
    
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
        data = eval(data)
        msg = {"msgname":data["msgname"], "entryID":data["entryID"], "accNum":data["msglist"][0], "accVal":data["msglist"][1]}
        return msg
    

    def promise(self):
        majority = []
        for acceptor_ip in self.acceptors_ip:
            data = self.UDP.recv(acceptor_ip, "promise")
            print data
            if data == None: continue
            #msg = eval(data)
            msg = translateMsg(data)
            
            if msg["msgname"] != "promise": continue
            if msg["accNum"] >= self.m : continue
            
            majority.append(msg)
        self.select_val(majority)
        print majority
        if len(majority)<=self.acceptors_num/2: return False
        else : return True
    
    def accept(self):
        msg = {"entryID":self.entryID, "msgname":"accept", "id":self.m, "val":self.v}
        for acceptor_ip in self.acceptors_ip:
            self.UDP.send(acceptor_ip, msg["msgname"], str(msg))
    
    def ack(self):
        majority = []
        for acceptor_ip in self.acceptors_ip:
            data = self.UDP.recv(acceptor_ip, "ack")
            if data == None: continue
            #msg = eval(data)
            msg = translateMsg(data)
            
            if msg["msgname"] != "ack": continue
            if msg["accNum"] != self.m : continue
            if msg["accVal"] != self.v : continue
            majority.append(msg)
        print majority
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

def test():
    #ports = {"prepare":12345, "promise":12346, "accept":12345, "ack":12348, "commit":12345, "request":12345, "update":12347}
    proposer = Proposer(random.randint(0,1)==0)
    proposer.allPhases()

test()
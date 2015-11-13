import udp
from configuration import Configuration as conf

class Acceptor:
    def __init__(self):
        self.proposer_ip = None
        self.acceptor_ips = conf.IPTABLE
        self.maxPrepare = 0
        self.accNum = 0
        self.accVal = None
        self.UDP = udp.UDP()

    def findProposer(self):
        for ip in self.acceptor_ips:
            print ip, "prepare"
            data = self.UDP.recv(ip, "prepare")
            if data!=None :
                self.proposer_ip = ip
                break
        return data

    def run(self):
        while(True):
            if self.proposer_ip == None:
                data = self.findProposer()
            else :
                data = self.UDP.recv(self.proposer_ip, "prepare")
            if data == None : continue
            recv_msg = eval(data)
            print recv_msg
            '''
            if recv_msg["msgname"]== "request":
                send_msg = {"entryID":recv_msg["entryID"], "msgname":"update", "maxPrepare":self.maxPrepare, "accNum":self.accNum, "accVal":self.accVal}
                self.UDP.send(self.proposer_ip, send_msg["msgname"], str(send_msg))
            el
            '''
            if recv_msg["msgname"]== "prepare":
                m = recv_msg["id"]
                if m > self.maxPrepare:
                    self.maxPrepare = m
                    send_msg = {"entryID":recv_msg["entryID"], "msgname":"promise", "accNum":self.accNum, "accVal":self.accVal}
                    self.UDP.send(self.proposer_ip, send_msg["msgname"], str(send_msg))
            elif recv_msg["msgname"]== "accept":
                m = recv_msg["id"]
                v = recv_msg["val"]
                if m >= self.maxPrepare:
                    self.accNum = m
                    self.accVal = v
                    send_msg = {"entryID":recv_msg["entryID"], "msgname":"ack", "accNum":self.accNum, "accVal":self.accVal}
                    self.UDP.send(self.proposer_ip, send_msg["msgname"], str(send_msg))
            elif recv_msg["msgname"]== "commit":
                v = recv_msg["val"]
                print "record:", v, "in log" #toDo

def test():
    #ports = {"prepare":12345, "promise":12346, "accept":12345, "ack":12348, "commit":12345, "request":12345, "update":12347}
    acceptor = Acceptor()
    acceptor.run()

test()
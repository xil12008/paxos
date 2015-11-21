import udp

class Acceptor:
    def __init__(self):
        self.proposer_ip = ''
        self.record = {}
        self.readlog()
        self.UDP = udp.UDP()

    def initRecord(self,key):
        self.record[key] = {}
        self.record[key]["maxPrepare"] = 0
        self.record[key]["accNum"] = 0
        self.record[key]["accVal"] = None

    def findProposer(self):
        for ip in self.acceptor_ips:
            data = self.UDP.recv(ip, "prepare")
            if data!=None :
                self.proposer_ip = ip
                break
        return data

    def run(self):
        while(True):
            data, addr = self.UDP.recv('', "prepare")
            if data == None : continue
            self.proposer_ip = addr[0]
            recv_msg = eval(data)
            print recv_msg
            entryID = recv_msg["entryID"]
            if entryID not in self.record: self.initRecord(recv_msg["entryID"])
            if recv_msg["msgname"]== "prepare":
                m = recv_msg["id"]
                if m > self.record[entryID]["maxPrepare"]:
                    self.record[entryID]["maxPrepare"] = m
                    self.savelog()
                    send_msg = {"entryID":entryID, "msgname":"promise", "accNum":self.record[entryID]["accNum"], "accVal":self.record[entryID]["accVal"]}
                    self.UDP.send(self.proposer_ip, send_msg["msgname"], str(send_msg))
                else :
                    send_msg = {"entryID":entryID, "msgname":"maxPrepare", "maxPrepare":self.record[entryID]["maxPrepare"]}
                    self.UDP.send(self.proposer_ip, send_msg["msgname"], str(send_msg))

            elif recv_msg["msgname"]== "accept":
                m = recv_msg["id"]
                v = recv_msg["val"]
                if m >= self.record[entryID]["maxPrepare"]:
                    self.record[entryID]["accNum"] = m
                    self.record[entryID]["accVal"] = v
                    self.savelog()
                    send_msg = {"entryID":entryID, "msgname":"ack", "accNum":self.record[entryID]["accNum"], "accVal":self.record[entryID]["accVal"]}
                    self.UDP.send(self.proposer_ip, send_msg["msgname"], str(send_msg))
            elif recv_msg["msgname"]== "commit":
                v = recv_msg["val"]
                self.record[entryID]["commitVal"] = v
                self.savelog()

    def savelog(self):
        f = open('acceptor.state', 'w')
        f.write(str(self.record))

    def readlog(self):
        try:
            f = open('acceptor.state', 'r')
            for line in f:
                self.record = eval(line)
        except:
            ""

def test():
    acceptor = Acceptor()
    acceptor.run()

test()
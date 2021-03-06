import Queue
import threading
from threading import Thread
from collections import deque
import json
import time

from view import View
from consumer import Consumer
from acceptor import Acceptor
from bullyalgorithm import bullyalgorithm 

import pdb

class Producer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.view = View()
        self.queue = self.readqueue() 

    def dataPass(self, cmds):
        if cmds[0]=="add":
            if self.view.time_int(cmds[3])>=self.view.time_int(cmds[4]):
                return False
            if cmds[1] in self.constructCalendar().keys():
                return False 
            return True
        elif cmds[0]=="del":
            if cmds[1] in self.constructCalendar().keys():
                return True
            return False
  
    def readlog(self):
        record = {}
        try:
            f = open('acceptor.state', 'r')
            for line in f:
                record = eval(line)
        finally:
            return record

    def constructCalendar(self, record = None):
        if not record: record = self.readlog()
        calendar = {} 
        for entryID in range(10000): 
            if entryID in record.keys():
                if "commitVal" in record[entryID].keys():
                    if record[entryID]["commitVal"]["operation"] == "add":
                        if record[entryID]["commitVal"]["app_name"] in calendar.keys():
                            print "Warning: add same appointment name for mulitiple times."
                            break
                        calendar[record[entryID]["commitVal"]["app_name"]] = record[entryID]["commitVal"]
                    elif record[entryID]["commitVal"]["operation"] == "del":
                        if not record[entryID]["commitVal"]["app_name"] in calendar.keys():
                            print "Warning: try to delete an non-exist appointment."
                            break
                        calendar.pop(record[entryID]["commitVal"]["app_name"], None)
        for key, ele in calendar.items():  
            self.convertDate(calendar[key])
        return calendar

    def run(self):
        print "Welcome"
        while True:
            cmd = raw_input("")
            cmds = cmd.strip().split()
            if not cmds: 
                print "Type something."
                continue 
            if cmds[0]=="add":
                if len(cmds)!=6:
                    warning = "format: add <calendar name> <day> <start time> <end time> <participant list>"
                    print warning
                    continue
                    #@TODO Conflict
                else:
                    if not self.dataPass(cmds):
                        print "Wrong Input"
                        continue
                    self.queue.put({"operation":"add", "app_name":cmds[1], "day":self.view.days_int(cmds[2]), "startTime":self.view.time_int(cmds[3]), "endTime":self.view.time_int(cmds[4]), "participants":set(cmds[5].split(','))})
                    self.savequeue()
                    print "Roger that. Your command queue:"
                    self.printqueue()
            elif cmds[0]=="del":
                if len(cmds)!=2:
                    warning = "format: del <calendar name>"
                    print warning
                    continue 
                else:
                    if not self.dataPass(cmds):
                        print "Wrong Input"
                        continue
                    self.queue.put({"operation":"del", "app_name":cmds[1]})
                    self.savequeue()
                    print "Roger that. Your command queue:"
                    self.printqueue()
            elif cmds[0]=="viewlocal":
                if len(cmds)!=1:
                    warning = "format: viewlocal"
                    print warning
                    continue
                else:
                    print "Roger that. Your local commited log:"
                    self.showCalendar()
                    print "Your calendar:"
                    print self.constructCalendar().keys()
            elif cmds[0]=="view":
                if len(cmds)!=1:
                    warning = "format: view"
                    print warning
                    continue
                else:
                    self.queue.put({"operation":"view"})
                    self.savequeue()
                    print "Roger that. Your command queue:"
                    self.printqueue()
            elif cmds[0]=="log":
                if len(cmds)!=1:
                    warning = "format: log"
                    print warning
                    continue
                else:
                    print "Roger that. Your local log:"
                    self.showCalendar(committed = False)
            elif cmds[0]=="queue":
                if len(cmds)!=1:
                    warning = "format: queue"
                    print warning
                    continue
                else:
                    print "Roger that. Your command FIFO queue:"
                    self.printqueue()
            else:
                print "Unknown command. Only accept add/del/view/log"
            print "-" * 32 
            time.sleep(1)

    def showCalendar(self, record = None, committed = True):
        if not record: record = self.readlog()
        try:
            print "<" * 25
            for entryID in range(10000): 
                if entryID in record.keys():
                    if committed:
                        if "commitVal" in record[entryID].keys():
                            self.convertDate(record[entryID]["commitVal"])
                            print entryID, " | ",
                            print record[entryID]["commitVal"].values()
                    else:
                        print entryID, ":", 
                        print record[entryID]
            print ">" * 25
        except:
            print "Empty"

    def convertDate(self, dictionary):
        if "day" in dictionary.keys(): 
            dictionary["day"] = self.view.days_str(dictionary["day"])
        if "startTime" in dictionary.keys():
            dictionary["startTime"] = self.view.time_str(dictionary["startTime"])
        if "endTime" in dictionary.keys():
            dictionary["endTime"] = self.view.time_str(dictionary["endTime"])

    def savequeue(self):
        f = open('user.queue', 'w')
        f.write(str(list(self.queue.queue)))

    def printqueue(self):
        print str(list(self.queue.queue))
    
    def readqueue(self):
        queue = Queue.Queue()
        try:
            f = open('user.queue', 'r')
            for line in f:
                queue.queue = deque(eval(line))
        except:
            ""
        finally:
            return queue

if __name__=="__main__":
    bullyalgorithm(opt=False)

    producer = Producer()
    producer.setDaemon(True)
    producer.start()

    consumer = Consumer(producer.queue)
    consumer.setDaemon(True)
    consumer.start()
 
    acceptor = Acceptor()
    acceptor.setDaemon(True)
    acceptor.start()
   
    while threading.active_count() > 0:
        time.sleep(0.1)


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

    def run(self):
        print "Welcome"
        while True:
            cmd = raw_input("")
            cmds = cmd.strip().split()
            if cmds[0]=="add":
                if len(cmds)!=6:
                    warning = "format: add <calendar name> <day> <start time> <end time> <participant list>"
                    print warning
                    continue
                    #@TODO Conflict
                else:
                    self.queue.put({"operation":"add", "app_name":cmds[1], "day":self.view.days_int(cmds[2]), "startTime":self.view.time_int(cmds[3]), "endTime":self.view.time_int(cmds[4]), "participants":cmds[5]})
                    self.savequeue()
                    print "Roger that."
            elif cmds[0]=="del":
                if len(cmds)!=2:
                    warning = "format: del <calendar name>"
                    print warning
                    continue 
                else:
                    self.queue.put({"operation":"del", "app_name":cmds[1]})
                    self.savequeue()
                    print "Roger that."
            elif cmds[0]=="view":
                if len(cmds)!=1:
                    warning = "format: view"
                    print warning
                    continue
                else:
                    print "Roger that. Your local calendar:"
                    self.showCalendar()
            elif cmds[0]=="log":
                if len(cmds)!=1:
                    warning = "format: log"
                    print warning
                    continue
                else:
                    print "Roger that. Your local log:"
                    self.showCalendar(committed = False)
            else:
                print "Unknown command. Only accept add/del/view/log"
            time.sleep(1)

    def showCalendar(self, committed = True):
        record = {}
        try:
            f = open('acceptor.state', 'r')
            for line in f:
                record = eval(line)
            print "<" * 25
            for entryID in range(1000000): 
                if entryID in record.keys():
                    if committed:
                        if "commitVal" in record[entryID].keys():
                            self.convertDate(record[entryID]["commitVal"])
                            print(json.dumps(record[entryID]["commitVal"]))
                    else:
                        print entryID, ":", 
                        print(json.dumps(record[entryID]))
            print ">" * 25
        except:
            print "Empty"

    def convertDate(self, dictionary):
        if "day" in dictionary.keys(): dictionary["day"] = self.view.days_str(dictionary["day"])
        if "startTime" in dictionary.keys(): dictionary["startTime"] = self.view.time_str(dictionary["startTime"])
        if "endTime" in dictionary.keys(): dictionary["endTime"] = self.view.time_str(dictionary["endTime"])

    def savequeue(self):
        f = open('user.queue', 'w')
        f.write(str(list(self.queue.queue)))
    
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


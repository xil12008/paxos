import Queue
import threading
from threading import Thread
from collections import deque
import time

from consumer import Consumer
from acceptor import Acceptor
from bullyalgorithm import bullyalgorithm 

class Producer(Thread):
    def __init__(self):
        Thread.__init__(self)
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
                    self.queue.put({"operation":"add", "app_name":cmds[1], "day":cmds[2], "startTime":cmds[3], "endTime":cmds[4], "participants":cmds[5]})
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
                    pass
                    print "Roger that."
            elif cmds[0]=="log":
                if len(cmds)!=1:
                    warning = "format: log"
                    print warning
                    continue
                else:
                    pass
                    print "Roger that."
            else:
                print "Unknown command. Only accept add/del/view/log"
            time.sleep(1)

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
    bullyalgorithm()

    producer = Producer()
    producer.start()

    consumer = Consumer(producer.queue)
    consumer.start()
 
    acceptor = Acceptor()
    acceptor.start()
   
    while threading.active_count() > 0:
        time.sleep(0.1)

import udp
import Queue
import random
from threading import Thread
import time
from configuration import Configuration as conf
from bullyalgorithm import TCPSend

class Consumer(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.event = None
        self.users_ip = conf.IPTABLE
        self.UDP = udp.UDP(30)
        self.queue = queue

    def getEvent(self):
        while self.queue.empty(): ""
        self.event = self.queue.queue[0]

    def popEvent(self):
        tmp = self.queue.get()
        print "**from command queue pop out:",tmp
        self.savequeue()

    def savequeue(self):
        f = open('user.queue', 'w')
        f.write(str(list(self.queue.queue)))
  
    def wait4leader(self): 
        while True:
          if conf.leader != -1:
              if TCPSend(conf.leader, "hi") == 0 : #alive leader found 
                  time.sleep(6)
                  print "wait4leader: alive leader found"
                  return
          time.sleep(1)

    def sendEvent(self):
        print "sendEvent: wait4leader"
        self.wait4leader() 
        for user in self.users_ip:
            self.UDP.send(user,"event",str(self.event))
        data,addr = self.UDP.recv('', "complete")
        if data == None : return False
        print "send event done, recved:", data, "from", addr
        return True

    def run(self):
        self.getEvent()
        while True:
            if not self.sendEvent() : continue
            print self.popEvent()
            print self.getEvent()
            time.sleep(1)

def getTime():
    startTime = 0
    endTime = 0
    while(startTime>=endTime):
        startTime = random.randint(0,10)
        endTime = random.randint(0,10)
    return startTime, endTime

def testConsumer():
    queue = Queue.PriorityQueue()
    startTime, endTime = getTime()
    queue.put({"operation":"add", "app_name":random.randint(0,1), "startTime":startTime, "endTime":endTime})
    consumer = Consumer(queue)
    consumer.start()

#testConsumer()

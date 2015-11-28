import udp
import Queue
import random
from threading import Thread
import time
from configuration import Configuration as conf

class Consumer(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.event = None
        self.users_ip = conf.IPTABLE
        self.UDP = udp.UDP()
        self.queue = queue
        self.getEvent()

    def getEvent(self):
        while self.queue.empty(): ""
        self.event = self.queue.queue[0]

    def popEvent(self):
        tmp = self.queue.get()
        self.savequeue()

    def savequeue(self):
        f = open('user.queue', 'w')
        f.write(str(list(self.queue.queue)))

    def sendEvent(self):
        for user in self.users_ip:
            self.UDP.send(user,"event",str(self.event))
        data,addr = self.UDP.recv('', "complete")
        if data == None : return False
        return True

    def run(self):
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

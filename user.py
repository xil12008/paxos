from threading import Thread, Condition
import time
import random

queue = []
MAX_NUM = 1000
condition = Condition()

class ProducerThread(Thread):
    def run(self):
        nums = range(5)
        global queue
        while True:
            condition.acquire()
            if len(queue) == MAX_NUM:
                print "Queue full, producer is waiting"
                condition.wait()
                print "Space in queue, Consumer notified the producer"
            num = raw_input(">>>")
            queue.append( num)
            print "Produced", num
            condition.notify()
            condition.release()
            time.sleep(random.random())

class ConsumerThread(Thread):
    def run(self):
        global queue
        while True:
            #self.top()
            self.pop()

    #call this function to query the first unprocessed user input
    def top(self):
        condition.acquire()
        if not queue:
            print "Nothing in queue, consumer is waiting"
            condition.wait()
            print "Producer added something to queue and notified the consumer"
        num = queue[0]
        print "top ", num
        condition.notify()
        condition.release()
        time.sleep(random.random())
        return

    #call this function to pop the first user input
    def pop(self):
            condition.acquire()
            if not queue:
                print "Nothing in queue, consumer is waiting"
                condition.wait()
                print "Producer added something to queue and notified the consumer"
            num = queue.pop(0)
            print "Consumed", num
            condition.notify()
            condition.release()
            time.sleep(random.random())

ProducerThread().start()
ConsumerThread().start()

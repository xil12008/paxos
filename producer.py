import Queue

class Prodcuer:
    def __init__(self, queue):
        self.queue = queue

    def run(self):
        while True:
            cmd = raw_input(">>>")
            cmds = cmd.strip().split()
            if cmds[0]=="add":
                if len(cmds)!=6:
                    warning = "format: add <calendar name> <day> <start time> <end time> <participant list>"
                    print warning
                    continue
                    #@TODO Conflict
                else:
                    self.queue.put({"operation":"add", "app_name":cmds[1], "day":cmds[2], "startTime":cmds[3], "endTime":cmds[4], "participants":cmds[5]})
            elif cmds[0]=="del":
                if len(cmds)!=2:
                    warning = "format: del <calendar name>"
                    print warning
                    continue 
                else:
                    self.queue.put({"operation":"del", "app_name":cmds[1]})
            elif cmds[0]=="view":
                if len(cmds)!=1:
                    warning = "format: view"
                    print warning
                    continue
                else:
                    pass


def testProducer():
    queue = Queue.Queue()
    producer = Producer(queue)
    producer.run()

testProducer()

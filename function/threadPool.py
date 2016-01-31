from threading import Thread,Lock
from Queue import Queue,Empty

class WorkThread(Thread):
    def __init__(self,threadPool):
        Thread.__init__(self)
        self.threadPool=threadPool
        self.daemon=True
        self.state=None
        self.start()

    def stop(self):
        if self.state=='STOP':
            self.state='STOP'
    def run(self):
        while 1:
            if self.state=='STOP':
                break
            try:
                func,args,kargs=self.threadPool.getTask(timeout=1)
            except Empty:
                continue
            try:
                self.threadPool.increaseRunsNum()
                result=func(*args,**kargs)
                self.threadPool.decreaseRunsNum()
                self.threadPool.taskDone()
            except Exception,e:
                print str(e)

class ThreadPool(object):
    def __init__(self,threadNum):
        self.threadNum=threadNum
        self.pool=[]
        self.lock=Lock()
        self.running=0
        self.taskQueue=Queue()
    def startThreads(self):
        for i in range(self.threadNum):
            self.pool.append(WorkThread(self))
    def stopThreads(self):
        for thread in self.pool:
            thread.stop()
            #thread.join()
        del self.pool[:]
    def putTask(self,func,*args,**kargs):
        self.taskQueue.put((func,args,kargs))
    def getTask(self,*args,**kargs):
        task=self.taskQueue.get(*args,**kargs)
        return task
    def taskJoin(self,*args,**kargs):
        self.taskQueue.join()
    def taskDone(self,*args,**kargs):
        self.taskQueue.task_done()
    def increaseRunsNum(self):
        self.lock.acquire()
        self.running+=1
        self.lock.release()
    def decreaseRunsNum(self):
        self.lock.acquire()
        self.running-=1
        self.lock.release()
    def getTaskLeft(self):
        return self.taskQueue.qsize()+self.running
def handler(param):
    print "404notfound",param

if __name__=="__main__":
    pass
    threadPool=ThreadPool(5)
    threadPool.startThreads()
    for i in range(100):
        threadPool.putTask(handler,'ToT')
    
    
    

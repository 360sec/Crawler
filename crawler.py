from collections import deque
import time
import re
import optparse
from function.threadPool import ThreadPool
from function.getLinks import GetLinks
from function.downLoadPage import DownLoadPage


class Crawler(object):
    def __init__(self,url,depth,model,thread,keyword=None):
        self.originalUrl=url
        #print self.originalUrl
        self.depth=depth
        self.model=model
        self.threadNum=thread
        self.keyword=str(keyword)
        self.currentDepth=0
        self.crawState=False
        self.threadPool=ThreadPool(self.threadNum)
        self.visitedUrls=set()
        self.unvisitedUrls=deque()
        self.unvisitedUrls.append(url)
        self.visitedUrls=[]
    def start(self):
        print "[START]Perhaps wait .......\n"
        self.crawState=True
        self.threadPool.startThreads()
        while self.currentDepth<=self.depth:
            
            self.assignCurrentDepthTasks()
            while self.threadPool.getTaskLeft():
                time.sleep(5)
            self.currentDepth+=1
        self.stop()
    def assignCurrentDepthTasks(self):
        while self.unvisitedUrls:
            url=self.unvisitedUrls.popleft()
            self.threadPool.putTask(self.task_handler,url)
            self.visitedUrls.append(url)
        print 'Depth %d Finish.Totally visited %d links\n' %(self.currentDepth,len(self.visitedUrls))
    def stop(self):
        self.crawState=False
        self.threadPool.stopThreads()
    def task_handler(self,url):
        downloadpage=DownLoadPage(url)
        if downloadpage.downloadpage(self.model):#default downloadpagemodel is static
            page,url=downloadpage.returnpage()
            getlinks=GetLinks(page,url)
            links=getlinks.getLinks(self.originalUrl)
            for link in links:
                self.outputData(link)
                self.unvisitedUrls.append(link)
    def outputData(self,url):#动态链接；子域名；keyword等过滤条件
        if self.keyword=='dynamic':
            if '?' in url:
                with open('dict.txt','a+') as file:
                    file.write(url+'\n')
                print url
        elif self.keyword=='subdomain':
            url=url.split('/')[2]#TODO filter domain
            print '[INFO]',url
        else:
            print '[INFO]',url
               

if __name__=="__main__":
    parser=optparse.OptionParser()
    parser.add_option('-u','--url',type='string',default='http://jwcad.ahut.edu.cn',help='Target URL(e.g. "http://www.xx00.com")')
    parser.add_option('-d','--depth',type='int',default=3,help='Depth of you want to test')
    parser.add_option('-m','--model',type='string',default='static',help='Model of you want to download page(e.g. -m Static or -m dynamic)')
    parser.add_option('-t','--thread',type='int',default=10,help='The thread num of ThreadPool')
    parser.add_option('-k','--keyword',type='string',help='The keyword you want to search.(eg:"?" can get dynamic links;"subdomain" can get subdomain;"all" can output all links) ')
    (options,args)=parser.parse_args()
    url=options.url
    depth=options.depth
    model=options.model
    thread=options.thread
    keyword=options.keyword
    if re.search(r'(http://)(\w+)([\.\w+]+)',url):
        crawler=Crawler(url,depth,model,thread,keyword)
        crawler.start()
        raw_input('Enter to continue')
    else:
        print "URL is error. eg:http://www.xxoo.com"
        

#!/usr/bin/python
#-*-coding:utf-8-*-
import requests
import time
import json


class AutoSqli(object):

    """
    使用sqlmapapi的方法进行与sqlmapapi建立的server进行交互

    
    """

    def __init__(self, server='', target='',data = '',referer = '',cookie = ''):
        super(AutoSqli, self).__init__()
        self.server = server
        if self.server[-1] != '/':
            self.server = self.server + '/'
        self.target = target
        self.taskid = ''
        self.engineid = ''
        self.status = ''
        self.data = data
        self.referer = referer
        self.cookie = cookie
        self.start_time = time.time()

    def task_new(self):
        self.taskid = json.loads(
            requests.get(self.server + 'task/new',timeout=10).text)['taskid']
        print 'Created new task: ' + self.taskid
        if len(self.taskid) > 0:
            return True
        return False

    def task_delete(self):
        if json.loads(requests.get(self.server + 'task/' + self.taskid + '/delete').text)['success']:
            print '[%s] Deleted task' % (self.taskid)
            return True
        return False

    def scan_start(self):
        headers = {'Content-Type': 'application/json'}
        payload = {'url': self.target}
        url = self.server + 'scan/' + self.taskid + '/start'
        t = json.loads(
            requests.post(url, data=json.dumps(payload), headers=headers,timeout=10).text)
        self.engineid = t['engineid']
        if len(str(self.engineid)) > 0 and t['success']:
            print 'Started scan'
            return True
        return False

    def scan_status(self):
        self.status = json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/status',timeout=10).text)['status']
        if self.status == 'running':
            return 'running'
        elif self.status == 'terminated':
            return 'terminated'
        else:
            return 'error'

    def scan_data(self):
        self.data = json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/data').text)['data']
        if len(self.data) == 0:
            print 'not injection:\t'
        else:
            print 'injection:\t' + self.target

    def option_set(self):
        headers = {'Content-Type': 'application/json'}
        option = {"options": {
                    "smart": True,
                    
                    }
                 }
        url = self.server + 'option/' + self.taskid + '/set'
        t = json.loads(
            requests.post(url, data=json.dumps(option), headers=headers).text)
        print t

    def scan_stop(self):
        json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/stop').text)['success']

    def scan_kill(self):
        json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/kill').text)['success']

    def run(self):
        if not self.task_new():
            return False
        self.option_set()
        if not self.scan_start():
            return False
        while True:
            if self.scan_status() == 'running':
                time.sleep(10)
            elif self.scan_status() == 'terminated':
                break
            else:
                break
            print time.time() - self.start_time
            
            print "test"
            
        self.scan_data()
        print time.time() - self.start_time

if __name__ == '__main__':
    with open('dict.txt','r') as file:
        for url in file:
            url=url.strip('\n')
            print url
            t = AutoSqli('http://127.0.0.1:8775', url)
            t.run()
    

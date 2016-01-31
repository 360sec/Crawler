import requests
import logging
from writeLog import writeLog
from randomHeaders import randomHeaders
from selenium import webdriver

class DownLoadPage(object):
    def __init__(self,url,headers=randomHeaders()):
        self.url=url
        self.page=None
        self.headers=headers
    def downloadpage(self,defaultDownLoadPageModel='static'):
        if defaultDownLoadPageModel=='static':####静态下载
            try:
                #print self.headers
                response=requests.get(self.url,headers=self.headers,timeout=10)
                #response.encoding='gbk'
                if response.status_code==requests.codes.ok:
                    self.page=response.text
                    return True
                else:
                    pass
                    #print "Page not avaliable.Status Code:%d URL:%s" %(response.status_code,response.url)          
            except Exception,e:
                #print str(e)
                logging.debug(str(e))
            return None
        elif defaultDownLoadPageModel=='dynamic':###动态解析
            try:
                browser=webdriver.PhantomJS(desired_capabilities={'phantomjs.page.settings.resourceTimeout': '5000'})
                browser.get(self.url)
                self.page=browser.page_source
                browser.quit()
                return True
            except Exception,e:
                return False
        else:
            print "defaultDownLoadPageModel is error"
    def returnpage(self):
        return self.page,self.url

if __name__=="__main__":
    pass
    downloadpage=DownLoadPage('http://jwcad.ahut.edu.cn',randomHeaders())
    if downloadpage.downloadpage('dynamic'):
        html,url=downloadpage.returnpage()
        print url,html

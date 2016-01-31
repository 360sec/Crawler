from downLoadPage import DownLoadPage
from urlFilter import UrlFilter
from urlparse import urljoin,urlparse
from bs4 import BeautifulSoup
import time
urlfilter=UrlFilter()

class GetLinks(object):
    def __init__(self,html,currentUrl):
        
        self.html=html
        self.links=[]
        self.currentUrl=currentUrl
        self.soup=BeautifulSoup(html)
    
    def getLinks(self,originalUrl,get='get'):
        #print "[INFO]:",self.currentUrl##################OUTPUT data
        if get=='get':
            results=self.soup.find_all('a',href=True)###get型：取a标签href属性
            for i in results:
                href=i.get('href')
                if not href.startswith('http'):
                    href=urljoin(self.currentUrl,href)
                if urlfilter.judgeUrlFormat(href,originalUrl):
                    if urlfilter.filterSameLink(href):###去重
                        if urlfilter.filterSimilarLink(href):##去相似
                            self.links.append(href)
                            
                else:
                    continue
                    #print self.currentUrl,' is similar'
            return self.links
        elif get=='post':
            pass
        else:
            print "只支持get和post"
    
if __name__=="__main__":
    downloadpage=DownLoadPage('http://jwcad.ahut.edu.cn')
    if downloadpage.downloadpage('dynamic'):
        html,url=downloadpage.returnpage()
    getlinks=GetLinks(html,url)
    links=getlinks.getLinks('http://jwcad.ahut.edu.cn')
    print links
    
    

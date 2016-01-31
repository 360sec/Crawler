import re
from bloom import BloomFilterJudge
from urlsimilar import urlsimilar
bloomFilterJudge1=BloomFilterJudge()
bloomFilterJudge2=BloomFilterJudge()
class UrlFilter(object):
    def __init__(self):
        pass
    def filterSameLink(self,link):
        if bloomFilterJudge1.determine(link):
            #print link," is unique link"
            return True
        else:

            return False
    def filterSimilarLink(self,link):
        key=urlsimilar(link)
        if bloomFilterJudge2.determine(str(key)):
            #print link,"is not similar"
            return True
        else:
            return False
    def judgeUrlFormat(self,link,originalUrl):
        
        if 'http' not in link:
            return False
        if link.split('.')[1]==originalUrl.split('.')[1]:
            if 'gif' not in (link.split('.')[-1]).lower() and 'doc' not in (link.split('.')[-1]).lower() and 'docx' not in (link.split('.')[-1]).lower() and 'pdf' not in (link.split('.')[-1]).lower() and 'swf' not in (link.split('.')[-1]).lower() and 'jpg' not in (link.split('.')[-1]).lower() and 'png' not in (link.split('.')[-1]).lower() and 'js' not in (link.split('.')[-1]).lower():
                return True
            else:
                return False
        elif re.search(r'(http://)\d+',link):
            return True
        else:
            return False
            #print link," donot belongs to rawUrl"
if __name__=="__main__":
    
    urlfilter=UrlFilter()
    if urlfilter.filterSimilarLink('http://www.95sec.com/1/2356/34.html'):
        print "True"
    if  not urlfilter.filterSimilarLink('http://www.95sec.com/1/6577/89.html'):
        print "False"
        
 


CrawlerV1.0

http://www.95sec.com

by 404 Not Found

email:root@95sec.com

#--------------------------------------------------------
该动态爬虫主要采用了

ThreadPool实现线程池；

requests库和selenium库加phantomJS实现页面的动静态下载；

Beautifulsoup库实现URL的提取；

BloomFilter实现URL去重；

urlsimilar实现URL去相似；

一些配置设置例如：randomHeaders和proxy，log日志等
#--------------------------------------------------------

Usage：
crawler.py -u url       

crawler.py -u url -d depth        

crawler.py -u url -d depth -m dynamic       

crawler.py -u url -d depth -m dynamic -t threadnum        

crawler.py -u url -d depth -m dynamic -t threadnum -k keyword 

eg:crawler.py -u http://www.wooyun.org -d 3 -m dynamic -t 10

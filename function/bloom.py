import BitVector
import os
import sys

class SimpleHash():
    def __init__(self,cap,seed):
        self.cap=cap
        self.seed=seed
        #print self.cap,self.seed
    def hash(self,value):
        ret=0
        #print len(value)
        for i in range(len(value)):
            ret+=self.seed*ret+ord(value[i])
        #print ret
        return (self.cap-1)&ret

class BloomFilter():
    def __init__(self,BIT_SIZE=1<<25):
        self.BIT_SIZE=1<<25
        self.seeds=[5,7,11,13,31,37,61]
        self.bitset=BitVector.BitVector(size=self.BIT_SIZE)
        self.hashFunc=[]

        for i in range(len(self.seeds)):
            #print i
            self.hashFunc.append(SimpleHash(self.BIT_SIZE,self.seeds[i]))
    def insert(self,value):
        for f in self.hashFunc:
            loc=f.hash(value)
            #print loc
            self.bitset[loc]=1
            #print self.bitset[loc]
    def isContaions(self,value):
        if value==None:
            return False
        ret=1
        for f in self.hashFunc:
            loc=f.hash(value)
            #print loc
            #print self.bitset[loc]
            ret=ret&self.bitset[loc]
            #rint ret
        #print ret
        return ret
bloomfilter=BloomFilter()

class BloomFilterJudge():
    
    def __init__(self):
        global bloomfilter
    def determine(self,url):
        if  bloomfilter.isContaions(url)==False:
            bloomfilter.insert(url)
            return True
        else:
            return False    

if __name__=="__main__":
    
    bloomfilterjudge=BloomFilterJudge()
    status=bloomfilterjudge.determine('http://www.95sec.com')
    print status
    status=bloomfilterjudge.determine('http://www.95sec.com')
    print status
    pass
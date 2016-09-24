#!/usr/bin/env python 
"""
@summary: this class is to implement the selection algorithm knowing or not knowning
        the stream length N in in prior
@note: This implementation is based on:
Guha, S., & McGregor, A. (2009). Stream Order and Order Statistics: 
Quantile Estimation in Random-Order Streams. 
SIAM Journal on Computing, 38(5), 2044. doi: 10.1137/07069328X.


@requires: n should be about larger than 7999999 (verified by Qiang)
"""

import math
import numpy as np

### compute the rank of given item in given array
def Rank(array, item):
    count = 0
    for i in xrange(len(array)):
        if array[i] < item:
            count += 1 
    return count + 1
    
    


### if we know the size of dataset, use this method
class KnowNEstimate:
    def __init__(self):
        self.a = -float("inf")
        self.b = float("inf") 
        self.gama = float(0.0)
        self.p = float(0.0)
        self.l1 = float(0.0)
        self.l2 = float(0.0)
        self.delta = float(0.99)
        self.N = float(0.0)
        self.k = float(0.0)
        self.phase = 0
        self.S = []
        self.E = []
        self.u = float(0.0)
        self.label = "Know-N"
        self.ests = []
        self.rankerrs = []
    
    ### input: n is the number of items in stream
    def SetUp(self, n, q):
        n *= 1.0
        self.k = math.ceil(n * q)
        self.N = n
        self.gama = 20.0 * math.pow(math.log(n), 2) * \
                    math.log(1.0 / self.delta) * math.sqrt(self.k)
        self.p = 4 * (math.log(n / self.gama, 4.0 / 3.0) + \
                       math.sqrt(math.log(3.0 / self.delta) * \
                        math.log(n / self.gama, 4.0 / 3.0)))
        self.l1 = n * 1.0 / self.gama * math.log(3 * n * n * self.p / self.delta)
        self.l2 = 2.0 * (n - 1) / self.gama * \
                math.sqrt((self.k + self.gama) * math.log(6.0 * n * self.p / self.delta))
    
    ### return current estimation
    def GetEstimate(self):
        return self.u

    ### reord estimation history
    def Record(self):
        self.ests.append(self.u)
    
    def RecordRankError(self, error):
        self.rankerrs.append(error)
    
    ### what happens every time a new item arrives
    def Update(self, d):
        ### collect sampled items
        if len(self.S) < self.l1:
            self.S.append(d)
        elif len(self.E) < self.l2:
            self.E.append(d)
        
        ### got enough items, let's adjust
        if len(self.S) >= self.l1 and len(self.E) >= self.l2:
            ### step (a), sample
            firstmeet = 0.0; found = False
            for item in self.S:
                if item > self.a and item < self.b:
                    self.u = item
                    found = True
                    break
            if not found:
                self.u = self.a
                
            ### step (b), estimate
            r = Rank(self.E, self.u)
            rnew = (self.N - 1) * (r - 1) / self.l2 + 1
            
            ### step (c), update
            if rnew < self.k - self.gama / 2:
                self.a = self.u
            if rnew > self.k + self.gama / 2:
                self.b = self.u
                
            ### after three setps, clear buffers
            self.S = []
            self.E = []
            self.phase += 1

        
### if we don't know the size of dataset
### in each phase, it actually calls KnowNEstimate to do the job
class UnkonwNEstimate:
    def __init__(self):
        self.beta = 1.5
        ### corresponds to i in algorithm
        self.guessnum = 0 ### the number of cur guess round number
        self.curlen = 0 ### in cur guess, how many items to look at
        self.totalsize = 0 ### number of items seen so far in total
        self.curguesssize = 0 ### num of items seen in cur guess round
        self.curstart = 0 ### the start item index in cur guess round
        self.curend = 0 ### the end item index in cur guess round
        self.u = float(0.0)
        self.q = 0.0
        self.knownest = KnowNEstimate()
        self.label = "Unknown-N"
        self.ests = []
        self.rankerrs = []
    
    ### return current estimation
    def GetEstimate(self):
        return self.u

    ### reord estimation history
    def Record(self):
        self.ests.append(self.u)
    
    def RecordRankError(self, error):
        self.rankerrs.append(error)
    
    def SetUp(self, q):
        self.q = q
        self.UpdateGuessPhase()
    
    ### update the len of current guess data size
    def UpdateGuessPhase(self):
        betapow = math.pow(self.beta, self.guessnum)
        self.curlen = math.ceil(4 * betapow) - math.floor(betapow) + 1
        self.curstart = math.floor(betapow)
        self.curend = math.ceil(4 * betapow)
         

    ### what happens when an item arrives
    def Update(self, d):
        self.totalsize += 1
        self.curguesssize += 1
        if self.curguesssize >= 2 * self.curlen:
            # print "Entering next guess round"
            self.curguesssize = 0
            self.guessnum += 1
            self.UpdateGuessPhase()
        else:
            if self.curguesssize == self.curstart:
                # print "Beginning of a guess round"
                self.knownest.SetUp(self.curlen, self.q)
                self.knownest.Update(d)
                self.u = self.knownest.GetEstimate()
            elif self.curguesssize < self.curend:
                # print "Inside current guess round active phase"
                self.knownest.Update(d)
                self.u = self.knownest.GetEstimate()
            # else:
            #     print "Inside current guess round inactive phase"
        
        
mu, sigma = 5000, 500
data = [int(x) for x in np.random.normal(mu, sigma, 8000000)]
q = 0.5

print 'Data true '+str(q)+'-quantile', sorted(data)[int(len(data)*q)]

print 'Knowning stream size'
knownest = KnowNEstimate()
knownest.SetUp(len(data), q)
for i in range(len(data)):
    if i % 1000000 == 0:
        print '\tEstimate:', knownest.GetEstimate()
    knownest.Update(data[i])

print '==========================\n'
print 'Without knowing stream size'

unknownest = UnkonwNEstimate()
unknownest.SetUp(q)
for i in range(len(data)):
    if i % 1000000 == 0:
        print '\tEstimate:', unknownest.GetEstimate()
    unknownest.Update(data[i])


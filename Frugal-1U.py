'''
@incollection{ma2013frugal,
  title={Frugal streaming for estimating quantiles},
  author={Ma, Qiang and Muthukrishnan, S and Sandler, Mark},
  booktitle={Space-Efficient Data Structures, Streams, and Algorithms},
  pages={77--96},
  year={2013},
  publisher={Springer}
}
'''
import random as rand
import numpy as np

class Frugal1U:
    def __init__(self, q):
        self.M = 0
        self.q = q
        self.label = "Frugal1U"
        self.ests = [] ### record estimation history
        self.rankerrs = []
    
    def GetEstimate(self):
        return self.M
    
    def Update(self, item):
        item = int(item)
        if item > self.M and rand.random() > 1 - self.q:
                self.M += 1
        elif item < self.M and rand.random() > self.q:
                self.M -= 1

    def Record(self, est=None):
        self.ests.append(self.M)
    
    def RecordRankError(self, error):
        self.rankerrs.append(error)
        
mu, sigma = 5000, 500
data = [int(x) for x in np.random.normal(mu, sigma, 100000)]
q = 0.5

print 'Data true '+str(q)+'-quantile', sorted(data)[int(len(data)*q)]

frugal1u = Frugal1U(q)
for i in range(len(data)):
    if i % 10000 == 0:
        print '\tEstimate:', frugal1u.GetEstimate()
    frugal1u.Update(data[i])

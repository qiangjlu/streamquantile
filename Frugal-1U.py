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
import random

class FindQuantile1U:
    def __init__(self, q):
        self.M = 0
        self.q = q
        self.label = "FindpQuantile-1U"
        self.ests = [self.label] ### record estimation history
        self.rankerrs = [self.labelerr]
    
    def GetEstimate(self):
        return self.M
    
    def Update(self, item):
        item = int(item)
        if item > self.M:
            if random.random() > 1 - self.q:
                self.M += 1
        elif item < self.M:
            if random.random() > self.q:
                self.M -= 1

    def Record(self, est=None):
        self.ests.append(self.M)
    
    def RecordRankError(self, error):
        self.rankerrs.append(error)

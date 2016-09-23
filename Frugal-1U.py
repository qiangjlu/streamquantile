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
    def __init__(self, quant, k):
        self.M = 0
        self.quant = float(quant)
        self.k = float(k)
        self.label = "FindpQuantile-1U"
        self.labelerr = self.label + "_rankerr"
        self.ests = [self.label] ### record estimation history
        self.rankerrs = [self.labelerr]
    
    def GetEstimate(self, N=None, quan=None, k=None):
        return self.M
    
    def Adjust(self, item):
        item = int(item)
        if item > self.M:
            if random.random() > 1 - self.quant / self.k:
                self.M += 1
        elif item < self.M:
            if random.random() > self.quant / self.k:
                self.M -= 1

    def Record(self, est=None):
        self.ests.append(self.M)
    
    def RecordRankError(self, error):
        self.rankerrs.append(error)

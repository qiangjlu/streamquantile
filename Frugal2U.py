'''
@incollection{ma2013frugal,
  title={Frugal streaming for estimating quantiles},
  author={Ma, Qiang and Muthukrishnan, S and Sandler, Mark},
  booktitle={Space-Efficient Data Structures, Streams, and Algorithms},
  pages={77--96},
  year={2013},
  publisher={Springer}
}


The implementation is also availale at blog post:
"Finding Quantiles With Two 'bits'- Frugal-2U"
https://research.neustar.biz/2013/09/16/sketch-of-the-day-frugal-streaming/
'''

import random as rand

class Frugal2U:
    def __init__(self, q):
        self.M = 0
        self.q = q
        self.step = 1
        self.sign = 1
        self.label = "Frugal2U"
        self.ests = [] ### record estimation history
        self.rankerrs = []
    
    def GetEstimate(self):
        return self.M
    
    def f(self, x):
        # Constant step size adjustment
        return 1
    
    def Update(self, item):
        if item > self.M and rand.random() > 1 - self.q:
            # Increment the step size if and only if the estimate keeps moving in
            # the same direction. Step size is incremented by the result of applying
            # the specified step function to the previous step size.
            self.step += self.f(self.step) if self.sign > 0 else -1 * self.f(self.step)
            # Increment the estimate by step size if step is positive. Otherwise,
            # increment the step size by one.
            self.M += self.step if self.step > 0 else 1
            # Mark that the estimate increased this step
            self.sign = 1
            # If the estimate overshot the item in the stream, pull the estimate back
            # and re-adjust the step size.
            if self.M > item:
                self.step += (item - self.M)
                self.M = item
        # If the item is less than the stream, follow all of the same steps as
        # above, with signs reversed.
        elif item < self.M and rand.random() > self.q:
            self.step += self.f(self.step) if self.sign < 0 else -1 * self.f(self.step)
            self.M -= self.step if self.step > 0 else 1
            self.sign = -1
            if self.M < item:
                self.step += (self.M - item)
                self.M = item
        
        # Damp down the step size to avoid oscillation.
        if (self.M - item) * self.sign < 0 and self.step > 1:
            self.step = 1

    def Record(self, est=None):
        self.ests.append(self.M)
    
    def RecordRankError(self, error):
        self.rankerrs.append(error)




mu, sigma = 5000, 500
data = [int(x) for x in np.random.normal(mu, sigma, 100000)]
q = 0.5

print 'Data true '+str(q)+'-quantile', sorted(data)[int(len(data)*q)]

frugal2u = Frugal2U(q)
for i in range(len(data)):
    if i % 10000 == 0:
        print '\tEstimate:', frugal2u.GetEstimate()
    frugal2u.Update(data[i])




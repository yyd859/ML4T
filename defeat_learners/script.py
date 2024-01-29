
import numpy as np
seed=5
np.random.seed(seed)
x = np.random.rand(100, 2)
y = np.sum(x, axis=1) + np.random.randn(100)
print (x[:,1])

x = np.random.rand(100, 2)
y = x[:,1]**2+x[:,0]**3 + np.random.randn(100)
print (y)
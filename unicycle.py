import pylab
import math
import numpy as np

C = np.array([0,1])

A = np.array([
		[0, 1],
		[0, 0],
	])


O = np.vstack((C, C.dot(A)))

print np.linalg.matrix_rank(O)

# Find vertices in an LP.

import numpy as np
n = 5

a0 = np.array([1,  0])
a1 = np.array([-1,  -2])
a2 = np.array([1,  2])
a3 = np.array([-1, 2])
a4 = np.array([3,  6])
A  = np.vstack((a0, a1, a2, a3, a4))
b  = np.array([2, -2, 6, -2, 18])


for i in xrange(n):
	for j in xrange(i+1, n):
		As = np.vstack((A[i, :],A[j, :]))
		bs = np.vstack((b[i], b[j]))
		r = np.linalg.matrix_rank(As)
		if r == 2:
			print np.matrix(As).I * bs
			print ""



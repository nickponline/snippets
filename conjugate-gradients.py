# Conjugate gradients to solve linear system.
# Can also minimize a quadratic form
# Ax = b, A is positive definite and symmetric

import numpy
import scipy

A  = numpy.array([[4, 1], [1, 3]])
b  = numpy.array([1, 2])
x  = numpy.array([2, 1])

r = b - A.dot(x) 
p = r
rsold = r.dot(r)


for i in xrange(10):
	Ap = A.dot(p)
	alpha = 1.0 * rsold / (p.dot(A).dot(p))
	x = x + alpha * p
	r = r - alpha * A.dot(p)
	rsnew = r.dot(r)

	if numpy.sqrt(rsnew) < 1e-10:
		break

	p = r + rsnew/rsold*p
	rsold = rsnew

print x


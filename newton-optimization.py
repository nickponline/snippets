import numpy as np
import pylab as pl


def objective1(x):
	return x*x*x, 3*x*x, 6*x

def objective(x):
	f = x[0]**2 + x[1]**2
	J = np.array([2*x[0], 2*x[1]])
	H = np.array([[2, 0], [0, 2]])
	return f, J, H

xx, yy = np.meshgrid(np.linspace(-100, 100, 100), np.linspace(-100, 100, 100))

zz, _, _ = objective([xx, yy])
pl.figure()
pl.contour(xx, yy, zz)


x0 = [np.array([10, 87])]

for i in xrange(100):
	prev = x0[-1]
	f, J, H = objective(prev)
	update = np.linalg.inv(H).dot(J)
	xn = prev - 0.1 * update.T
	x0.append(xn)


pl.plot([x[0] for x in x0], [x[1] for x in x0], )

x = np.linspace(-100, 100, 100)
y, _, _ = objective1(x)
x0 = [75.0]
for i in xrange(10):
	prev = x0[-1]
	f, J, H = objective1(prev)
	update = J / H
	xn = prev - update
	x0.append(xn)


y0 = map(lambda k: objective1(k)[0], x0)

pl.figure()
pl.plot(x, y)
pl.plot(x0,y0, 'r')
pl.show()


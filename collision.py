# Rotate a point around another one.   

import pylab as pl
import numpy as np
import random


def sqr(x):
	return x*x

def dist(a, b):
	return np.sqrt(sqr(a[1] - b[1]) + sqr(a[0] - b[0]))

def approx_zero(x, eps=0.0001):
	return np.abs(x) < eps

def rotate(point, anchor, angle):
	tau = np.arctan2(point[1] - anchor[1], point[0] - anchor[0]) + angle
	hyp = np.sqrt(sqr(point[1] - anchor[1]) + sqr(point[0] - anchor[0]))	
	rotated = anchor[0] + hyp * np.cos(tau), anchor[1] + hyp * np.sin(tau)
	return rotated

def ccw(A,B,C, includes=True):
	if includes:
		return (C[1]-A[1])*(B[0]-A[0]) >= (B[1]-A[1])*(C[0]-A[0])
	else:
		return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

def segment_segment_intersect(A,B,C,D,includes=True):
        return ccw(A,C,D, includes) != ccw(B,C,D,includes) and ccw(A,B,C,includes) != ccw(A,B,D,includes)

def segment_polygon_intersect(A,B,polygon,includes=True):
		N = len(polygon)
		return True in [segment_segment_intersect(A, B, polygon[i], polygon[(i+1) % N],includes) for i in xrange(N)]

# TODO: One circle inside the other
def circle_circle_intersect(p0, r0, p1, r1, includes=True):

	d = dist(p0, p1)
	eps = 0.00001

	if d > (r0+r1):
		print "No intersections, separate."
		return None
	elif d < np.abs(r0-r1):
		print "No intersections, concentric."
		return None
	elif approx_zero(d) and approx_zero(dist(p0, p1)):
		print "Infinite intersections."
		return None

	print "Two intersections."

	x0, y0 = p0
	x1, y1 = p1

	dx = x1 - x0
	dy = y1 - y0

	d = np.sqrt((dy*dy) + (dx*dx));
 
	a = ((r0*r0) - (r1*r1) + (d*d)) / (2.0 * d)

	x2 = x0 + (dx * a/d);
	y2 = y0 + (dy * a/d);

	h = np.sqrt(np.abs((r0*r0) - (a*a)))

	rx = -dy * (h/d);
	ry = dx * (h/d);

	xi = x2 + rx;
	yi = y2 + ry;
	pl.plot(xi, yi, 'rx')

	xi = x2 - rx;
	yi = y2 - ry;
	pl.plot(xi, yi, 'rx')

def plot_segment(A, B, style='k'):
	pl.plot([A[0], B[0]], [A[1], B[1]], style)

def plot_circle(C, R, style='k'):
	polygon_approximation = [ (C[0] + R * np.cos(i * np.pi/180.0), C[1] + R * np.sin(i * np.pi/180.0)) for i in np.linspace(0.0, 360.0, 300)]
	plot_polygon(polygon_approximation, style)

def plot_polygon(polygon, style='k'):
	N = len(polygon)

	for i in xrange(N):
		plot_segment(polygon[i], polygon[(i+1) % N], style)

	
# pl.figure()

# X = 6
# Y = 6

# for i in xrange(1, X*Y+1):
# 	pl.subplot(X, Y, i)

# 	A = random.random(), random.random()
# 	B = random.random(), random.random()
# 	C = random.random(), random.random()
# 	D = random.random(), random.random()

# 	if segment_segment_intersect(A, B, C, D):
# 		style = 'r'
# 	else:
# 		style = 'g'

# 	plot_segment(A, B, style)
# 	plot_segment(C, D, style)
	
# pl.show()



# X = 3
# Y = 3

# pl.figure()

# for i in xrange(1, X*Y+1):
# 	pl.subplot(X, Y, i)

# 	A = random.random(), random.random()
# 	B = random.random(), random.random()
	
# 	polygon = [(random.random() * np.cos(i * np.pi / 180.0), random.random() * np.sin(i * np.pi / 180.0)) for i in np.linspace(0, 360, 10)]

# 	if segment_polygon_intersect(A, B, polygon):
# 		style = 'r'
# 	else:
# 		style = 'g'

# 	plot_segment(A, B, style)
# 	plot_polygon(polygon, style)

# pl.show()




X = 3
Y = 3

pl.figure()

C1 = random.random(), random.random()
R1 = 0.5 + random.random()
C2 = random.random(), random.random()
R2 = 0.5 + random.random()
	
plot_circle(C1, R1)
plot_circle(C2, R2)

circle_circle_intersect(C1, R1, C2, R2)
pl.axis('equal')
pl.show()
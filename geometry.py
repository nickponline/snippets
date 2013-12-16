# Awesome attempt at robot motion planning.    
# Sample points near the bot as integer coords to they are cache able.
# Plug into A* algorithm. 
# Need a heuristic of visible maze distance
# Needs a code clean.

import pylab as pl
import numpy as np
import random	

def sqr(x):
	return x*x

def dist(a, b):
	return np.sqrt(sqr(a[1] - b[1]) + sqr(a[0] - b[0]))

def approx_zero(x, eps=0.0001):
	return np.abs(x) < eps

# rotate a point around an anchor by angle (rads) and return the new point
def rotate(point, anchor, angle):
	tau = np.arctan2(point[1] - anchor[1], point[0] - anchor[0]) + angle
	hyp = np.sqrt(sqr(point[1] - anchor[1]) + sqr(point[0] - anchor[0]))	
	rotated = anchor[0] + hyp * np.cos(tau), anchor[1] + hyp * np.sin(tau)
	return rotated

# above for list of points
def rotate_points(points, anchor, angle):
	func = lambda h: rotate(h, anchor, angle)
	return map(func, points)
	#return [rotate(point, anchor, angle) for point in points]

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

def polygon_polygon_itersect(poly_a, poly_b, includes=True):

    m = len(poly_a)
    n = len(poly_b)

    for i in xrange(m):
        if segment_polygon_intersect(poly_a[i], poly_a[(i+1) % m], poly_b, includes):
            return True

	for i in xrange(n):
		if segment_polygon_intersect(poly_b[i], poly_b[(i+1) % n], poly_a, includes):
			return True

	return False


def plot_segment(A, B, style='k'):
	pl.plot([A[0], B[0]], [A[1], B[1]], style)

def plot_polygon(polygon, style='k'):
	N = len(polygon)

	for i in xrange(N):
		plot_segment(polygon[i], polygon[(i+1) % N], style)

def rads(d):
	return d * np.pi / 180.0

def rotate_move(point, angle, r, d):
	return ( point[0] + d * np.cos(angle + rads(r)), point[1] + d * np.sin(angle + rads(r)))

def on_click(event):
	print 'Clicked: %d, X=%d, Y=%d, Xdata=%f, Ydata=%f' % (event.button, event.x, event.y, event.xdata, event.ydata)

def on_press(event):
	print 'Pressed: %s, X=%d, Y=%d, Xdata=%f, Ydata=%f' % (event.key, event.x, event.y, event.xdata, event.ydata)

def rand_poly(n=5, x=0.0, y=0.0):
	pts = []
	for i in xrange(n):
		k = 360.0 / n * i * np.pi / 180.0
		pts.append((x + np.cos(k) * random.random(), y + np.sin(k) * random.random(), ))	
	return pts

fig = pl.figure()
cid = fig.canvas.mpl_connect('button_press_event', on_click)
cid = fig.canvas.mpl_connect('key_press_event', on_press)

pl.clf()

pl.axis([-1, 3, -1, 3])


K = 5
p = [rand_poly(n=5, x=2*random.random(), y=2*random.random()) for i in xrange(K)] 
c = [True] * K

for i in xrange(0, len(p)):
    for j in xrange(i+1, len(p)):
        if polygon_polygon_itersect(p[i], p[j]):
        	c[i] = False
        	c[j] = False

for i, q in enumerate(p):
	if c[i]:
		plot_polygon(q, style='g')
	else:
		plot_polygon(q, style='r')
pl.draw()
pl.show()
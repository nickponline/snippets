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

def rotate(point, anchor, angle):
	tau = np.arctan2(point[1] - anchor[1], point[0] - anchor[0]) + angle
	hyp = np.sqrt(sqr(point[1] - anchor[1]) + sqr(point[0] - anchor[0]))	
	rotated = anchor[0] + hyp * np.cos(tau), anchor[1] + hyp * np.sin(tau)
	return rotated

def rotatePoint(points, anchor, angle):
	return [rotate(point, anchor, angle) for point in points]

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

def segments_intersect(A,B,segments,includes=True):
		for a, b in segments:
			if segment_segment_intersect(A, B, a, b):
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

def rotateMove(point, angle, r, d):
	return ( point[0] + d * np.cos(angle + rads(r)), point[1] + d * np.sin(angle + rads(r)))

class Wheelchair:
	def __init__(self, chair_x, chair_y, chair_dir, goal_x, goal_y):
		
		self.chair     = (chair_x, chair_y)
		self.chair_dir = chair_dir
		self.geometry = []
		self.goal_x = goal_x
		self.goal_y = goal_y
		self.update()

	
	def update(self):
		self.geometry = []
		axle_a = rotateMove(self.chair, self.chair_dir,  90, 0.5)
		axle_b = rotateMove(self.chair, self.chair_dir, -90, 0.5)

		wheel1_a = rotateMove(axle_a, self.chair_dir,  0,   0.5)
		wheel1_b = rotateMove(axle_a, self.chair_dir,  180, 0.5)
		wheel2_a = rotateMove(axle_b, self.chair_dir,  0,   0.5)
		wheel2_b = rotateMove(axle_b, self.chair_dir,  180, 0.5)
		
		box_a = rotateMove(self.chair, self.chair_dir, -90, 0.25)
		box_b = rotateMove(box_a, self.chair_dir, -90+90, 1)
		box_c = rotateMove(box_b, self.chair_dir, -90+90+90, 0.5)
		box_d = rotateMove(box_c, self.chair_dir, -90+90+90+90, 1)
			
		self.geometry.append((axle_a, axle_b))
		self.geometry.append((wheel1_a, wheel1_b))
		self.geometry.append((wheel2_a, wheel2_b))

		self.geometry.append((box_a,box_b))
		self.geometry.append((box_b,box_c))
		self.geometry.append((box_c,box_d))
		self.geometry.append((box_d,box_a))

		if dist(self.chair, (self.goal_x, self.goal_y)) < 0.5:
			print "Solved!"
		else:
			pass

	def isSolved(self):
		if dist(self.chair, (self.goal_x, self.goal_y)) < 0.5:
			return True
		else:
			return False

	def plot(self):
		for a, b in self.geometry:
			plot_segment(a,b)
			

	def rotate(self, angle):
		old_chair = self.chair
		old_chair_dir = self.chair_dir
		self.chair_dir = self.chair_dir + rads(angle)
		self.update()

		reverse = False
		for a, b in self.geometry:
			if segments_intersect(a, b, segs):
				reverse = True
				break

		if reverse:
			self.chair = old_chair
			self.chair_dir = old_chair_dir
			self.update()
			return False

		return True
			

	def push(self, d):
		old_chair = self.chair
		old_chair_dir = self.chair_dir
		self.chair     = (self.chair[0] + d*np.cos(self.chair_dir), self.chair[1] + d*np.sin(self.chair_dir))
		self.update()

		reverse = False
		for a, b in self.geometry:
			if segments_intersect(a, b, segs):
				reverse = True
				break
		
		if reverse:
			#print "CRASH!"
			self.chair = old_chair
			self.chair_dir = old_chair_dir
			self.update()
			return False

		return True



	def auto(self, point, move=False):
		#print "Cruis control to: ", point
		old_chair = self.chair
		old_chair_dir = self.chair_dir
		
		tau = np.arctan2(point[1] - self.chair[1], point[0] - self.chair[0])
		#print tau * 180.0 / np.pi
		#print self.chair_dir * 180.0 / np.pi
		tau =  (tau - self.chair_dir) * 180.0 / np.pi
		#print tau
		dis = dist(self.chair, point)
		incs = 10

		reset = False
		for i in xrange(incs):
			ret = self.rotate(tau / float(incs))
			#print "ROTATED: ", tau / float(incs)
			if not ret:
				reset = True
				#print "BUMP on ROTATION: ", i

		if reset:
			#print "Resetting!"
			self.chair = old_chair
			self.chair_dir = old_chair_dir
			self.update()
			for i in xrange(incs):
				ret = self.rotate((2.0 * np.pi - tau) / float(incs))
				if not ret:
					reset = True
					#print "BUMP on rev ROTATION: ", i

		if not reset:
			for i in xrange(incs):
				ret = self.push(dis / float(incs))
				if not ret:
					reset = True
					#print "BUMP on PUSH: ", i

		if not move:
			self.chair = old_chair
			self.chair_dir = old_chair_dir
			self.update()
			return not reset
		# move to point in increments checking for colision

data = open("/Users/nickp/Downloads/PROBLEMSET/input/L/1").read().strip().split("\n")
print data
walls, chair_x, chair_y, chair_r, goal_x, goal_y = map(float, data[0].split())
segs = []
lx =  10000
ly =  10000
ux = -10000
uy = -10000
for i in xrange(1, len(data)):
	a, b, c, d = map(float, data[i].split())

	lx = min(lx, a)
	lx = min(lx, c)
	ux = max(ux, a)
	ux = max(ux, c)

	ly = min(ly, b)
	ly = min(ly, d)
	uy = max(uy, b)
	uy = max(uy, d)

	segs.append(((a, b), (c, d)))

	w = Wheelchair(chair_x, chair_y, chair_r, goal_x, goal_y)

def onclick(event):
	print 'Clicked: %d, X=%d, Y=%d, Xdata=%f, Ydata=%f' % (event.button, event.x, event.y, event.xdata, event.ydata)
	
	ret = w.auto((event.xdata, event.ydata), move=True)
	pl.clf()
	pl.axis('equal')

	for a, b in segs:
		plot_segment(a, b)
	
	w.plot()
	pl.plot(goal_x, goal_y, 'xg')
	
	pl.draw()

cache = {}
def rec(w, path, steps, cache):

	if steps > 8:
		return None

	if cache.get((w.chair, w.chair_dir), None) == None:
		print "PATH TO: ", w.chair, w.chair_dir, "IS", path
		cache[(w.chair, w.chair_dir)] = path
	else:
		#print "ALREADY SEEN ", w.chair, w.chair_dir
		return None

	if w.isSolved():
		print "SOLVED!"
		print "SOLUTION: ", path
		return None

	n = Wheelchair(w.chair[0], w.chair[1], w.chair_dir, w.goal_x, w.goal_y)
	n.push(1)
	rec(n, path + ["FORD"], steps + 1, cache)

	n = Wheelchair(w.chair[0], w.chair[1], w.chair_dir, w.goal_x, w.goal_y)
	n.push(-1)
	rec(n, path + ["BACK"], steps + 1, cache)

	n = Wheelchair(w.chair[0], w.chair[1], w.chair_dir, w.goal_x, w.goal_y)
	n.rotate(10)
	rec(n, path + ["LEFT"], steps + 1, cache)

	n = Wheelchair(w.chair[0], w.chair[1], w.chair_dir, w.goal_x, w.goal_y)
	n.rotate(-10)
	rec(n, path + ["RIGHT"], steps + 1, cache)

def onpress(event):
	pl.clf()
	pl.axis('equal')


	print "Pressed: ", event.key
	if event.key == "up":
		w.push(1)
	elif event.key == "down":
		w.push(-1)
	elif event.key == "left":
		w.rotate(10)
	elif event.key == "right":
		w.rotate(-10)

	elif event.key == "a":
		for i in np.linspace(w.chair[0]-5, w.chair[0]+5, 15):
			print "PROGRESS:", i
			for j in np.linspace(w.chair[1]-5, w.chair[1]+5, 15):
				#if dist((i, j), w.chair) < 3.0:		
				ret = w.auto((i, j))
				if ret:
					pl.plot(i, j, 'g+')
	
	elif event.key == "r":
		cache = {}
		rec(w,[],0, cache)
		bestKey = None
		bestDistance = 10000
		for location, angle in cache.keys():
			if (bestKey == None) or (dist(location, (w.goal_x, w.goal_y)) < bestDistance):
				bestDistance = dist(location, (w.goal_x, w.goal_y)) 
				bestKey = (location, angle)
		print "Best so far: ", bestDistance, bestKey, cache[bestKey]
		pl.plot([w.chair[0], bestKey[0][0]], [w.chair[1], bestKey[0][1]], ':k')
		pl.plot(bestKey[0][0], bestKey[0][1], '+r')
	for a, b in segs:
		plot_segment(a, b)
	w.plot()
	pl.plot(goal_x, goal_y, 'xg')
	pl.draw()
	
	
fig = pl.figure()
cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid = fig.canvas.mpl_connect('key_press_event', onpress)


pl.clf()
pl.axis('equal')

for a, b in segs:
	plot_segment(a, b)
	
w.plot()
pl.plot(goal_x, goal_y, 'xg')
pl.draw()

pl.show()
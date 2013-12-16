# Rotate a point around another one.   

import pylab as pl
import numpy as np

def sqr(x):
	return x*x

def rotate(point, anchor, angle):
	tau = np.arctan2(point[1] - anchor[1], point[0] - anchor[0]) + angle
	hyp = np.sqrt(sqr(point[1] - anchor[1]) + sqr(point[0] - anchor[0]))	
	rotated = anchor[0] + hyp * np.cos(tau), anchor[1] + hyp * np.sin(tau)
	return rotated

def rotatePoint(points, anchor, angle):
	return [rotate(point, anchor, angle) for point in points]

anchor = (10, 5)
point  = (67, 50)

pl.figure()
pl.plot(anchor[0], anchor[1], 'ko')
pl.plot(point[0], point[1], 'ro')
pl.plot([point[0], anchor[0]], [point[1], anchor[1]], 'k:')

for angle in np.linspace(0, 360, 10):
	rotated = rotate(point, anchor, angle * np.pi / 180.0)
	pl.plot(rotated[0], rotated[1], 'go')
	pl.plot([rotated[0], anchor[0]], [rotated[1], anchor[1]], 'k:')

pl.title('Rotating Red to Green')
pl.show()
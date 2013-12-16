import numpy as np
import scipy.io.wavfile
import numpy.fft
import pylab
import math

length = 6500
skip   = 500
path   = "PROBLEMSET/input/E/example.wav"

def distance(x1, y1, x2, y2):
	return np.sqrt(np.power(x1-x2, 2.0) + np.power(y1-y2, 2.0))

def distance_squared(x1, y1, x2, y2):
	return np.power(x1-x2, 2.0) + np.power(y1-y2, 2.0)

def mytan(x, y):
	z = math.atan2(x, y)
	if (z < 0.0):
		return -z * 180 / np.pi
	else:
		return 360.0 - (z * 180.0 / np.pi)

def to360(x):
	while(x > 360.0):
		x = x - 360.0
	while(x < 0.0):
		x = x + 360.0
	return x


def goertzel(samples, target_frequency, sample_rate):
	s_prev = 0 
	s_prev2 = 0 
	normalized_frequency = 1.0 * target_frequency / sample_rate 
	coeff = 2.0 * np.cos(2.0 * np.pi * normalized_frequency) 
	for sample in samples:
	  s = sample + coeff * s_prev - s_prev2
	  s_prev2 = s_prev
	  s_prev = s
	power = s_prev2 * s_prev2 + s_prev * s_prev - coeff * s_prev * s_prev2
	return power


sample_rate, data = scipy.io.wavfile.read(path)

location_x = -179.4
location_y = -95.3

towers = [(0.0,0.0,350),(300.0,173.2,485),(-300.0,173.2,633),(-0.0,-346.4,796),(0.0,346.4,976),(-300.0,-173.2,1174),(300.0,-173.2,1391),(-200.0,-0.0,1630),(100.0,-173.2,1893),(100.0,173.2,2183),(-100.0,-173.2,2501),(200.0,0.0,2851),(-100.0,173.2,3236)]

fig = pylab.figure()
pylab.gca().axis('equal')
pylab.plot(location_x, location_y, 'or')
fig.canvas.draw()

test_x = 0.0
test_y = 0.0
average_x = []
average_y = []

for tower_x, tower_y, tower_f in towers:
	guessInitialDegree = -180.0

	windows = [data[startPos:startPos+length] for startPos in xrange(0, len(data) - length, skip)] 
	fourier = np.array([goertzel(w, tower_f, sample_rate) for w in windows], dtype=np.float64)
	n       = len(fourier)
	time    = np.arange(n, dtype=np.float64) / n * len(data) / sample_rate

	peakIndex  = np.argmax(fourier)
	print "PK: ", peakIndex

	for i, v in enumerate(fourier / fourier.max()):
		if (v > 0.98):
			peakIndex = i
			peakTime   = time[peakIndex]
			peakDegree = peakTime * 360.0

			dist = distance(tower_x, tower_y, location_x, location_y)
			speedSoundTime   = distance(tower_x, tower_y, location_x, location_y) / 340.29 #second
			speedSoundDegree = speedSoundTime * 360.0
			
			# pylab.subplot(3, 1, 1)
			# pylab.title('Signal at receiver')
			# pylab.plot(time, fourier,'r') # plotting the spectrum
			# pylab.xlabel('Time (s)')
			# pylab.ylabel('|Power|')
			# pylab.axis([-speedSoundTime,5,0,7e13])

			# pylab.subplot(3, 1, 2)
			# pylab.title('Signal at sender')
			# pylab.plot(time - speedSoundTime, fourier,'r') # plotting the spectrum
			# pylab.xlabel('Time (s)')
			# pylab.ylabel('|Power|')
			# pylab.axis([-speedSoundTime,5,0,7e13])
			# pylab.show()

			stime = time - speedSoundTime
			offset = stime[peakIndex] * 360.0

			print "True direction from this tower:", to360(mytan(location_x-tower_x, location_y-tower_y))
			print "With initial guess of", guessInitialDegree, " we are in the direction of:", to360(guessInitialDegree + offset)

			pylab.plot(tower_x, tower_y, '+k')
			angle = to360(guessInitialDegree + offset)
			test_x = tower_x + (dist * np.cos((90.0+angle) * np.pi / 180.0))
			test_y = tower_y + (dist * np.sin((90.0+angle) * np.pi / 180.0))

			pylab.plot([tower_x, test_x], [tower_y, test_y], 'r:')
			fig.canvas.draw()

			average_x.append(test_x)
			average_y.append(test_y)

# mean_x = sum(average_x) / len(towers)
# mean_y = sum(average_y) / len(towers)

# average_x = sorted(average_x, key= lambda h: abs(mean_x - h))
# average_y = sorted(average_y, key= lambda h: abs(mean_y - h))

for l in xrange(len(average_x)):
	t_x = average_x[l]
	t_y = average_y[l]	
	pylab.plot(t_x, t_y, '+g')

pylab.savefig('geometry.pdf')	
pylab.show()

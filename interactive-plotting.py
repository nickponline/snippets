import pylab as plt
import numpy as np

fig = plt.figure()
plt.plot(np.random.rand(10))

def onclick(event):
	plt.clf()
	plt.plot(np.random.rand(10))
	plt.draw()
	print 'Clicked: %d, X=%d, Y=%d, Xdata=%f, Ydata=%f' % (event.button, event.x, event.y, event.xdata, event.ydata)

def onpress(event):
	plt.clf()
	plt.plot(np.random.rand(10))
	plt.draw()
	print "Pressed: ", event.key

cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid = fig.canvas.mpl_connect('key_press_event', onpress)

plt.show()
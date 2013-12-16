import pylab

def onclick(event):
	print 'Clicked: %d, X=%d, Y=%d, Xdata=%f, Ydata=%f' % (event.button, event.x, event.y, event.xdata, event.ydata)
	
def onpress(event):
	print "Pressed: ", event.key
	
fig = pylab.figure()

cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid = fig.canvas.mpl_connect('key_press_event', onpress)

pylab.plot(10.0, 10.0, 'xg')
pylab.show()
"""
 Fourier transform and inverse.
"""

import numpy
import scipy
import pylab

Fs = 100.0
Ts = 1.0/Fs

t = numpy.arange(0.0, 1.0, Ts)
y = 20 * numpy.sin(2 * numpy.pi * 5.0 * t)

n = len(t)
k = numpy.arange(n)
T = n/Fs
f = k/T
f = f[range(n/2)]
Y = scipy.fft(y)
Y = Y/n*2.0
r = scipy.ifft(Y)*n/2.0
Y = abs(Y)
Y = Y[range(n/2)]
p = Y ** 2.0


pylab.figure()
pylab.subplot(4, 1, 1)
pylab.title("Original Signal")
pylab.plot(t, y)

pylab.subplot(4, 1, 2)
pylab.title("Frequency Spectrum")
pylab.plot(f, Y)

pylab.subplot(4, 1, 3)
pylab.title("Power Spectrum")
pylab.plot(f, p)

pylab.subplot(4, 1, 4)
pylab.plot(t, r)
pylab.title("Reconstruction")
pylab.show()
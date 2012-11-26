"""
  Goertzel algorithm
"""

import numpy as np
import scipy.signal
import scipy.io.wavfile
import pickle
from pylab import *

def goetrzel(x, target_frequency, sample_rate):
	s_prev = 0
	s_prev2 = 0
	normalized_frequency = target_frequency / sample_rate
	coeff = 2.0 * np.cos(2.0 * np.pi * normalized_frequency)
	for sample in x:
	  s = sample + coeff * s_prev - s_prev2
	  s_prev2 = s_prev
	  s_prev = s
	power = s_prev2 * s_prev2 + s_prev * s_prev - coeff * s_prev * s_prev2 ;
	return power

sample_rate, data = scipy.io.wavfile.read("example.wav")
spec = goetrzel(data, 2000.0, sample_rate)
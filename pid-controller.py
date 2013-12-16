import pylab as pl
import random

A = 1.25
B = 0.45
C = 89.50

class PID:
	"""
	Discrete PID control
	"""

	def __init__(self, P=2.0, I=0.0, D=1.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500):

		self.Kp=P
		self.Ki=I
		self.Kd=D
		self.Derivator=Derivator
		self.Integrator=Integrator
		self.Integrator_max=Integrator_max
		self.Integrator_min=Integrator_min

		self.set_point=0.0
		self.error=0.0

	def update(self,current_value):
		"""
		Calculate PID output value for given reference input and feedback
		"""

		self.error = self.set_point - current_value

		self.P_value = self.Kp * self.error
		self.D_value = self.Kd * ( self.error - self.Derivator)
		self.Derivator = self.error

		self.Integrator = self.Integrator + self.error

		if self.Integrator > self.Integrator_max:
			self.Integrator = self.Integrator_max
		elif self.Integrator < self.Integrator_min:
			self.Integrator = self.Integrator_min

		self.I_value = self.Integrator * self.Ki

		PID = self.P_value + self.I_value + self.D_value

		return PID

	def setPoint(self,set_point):
		"""
		Initilize the setpoint of PID
		"""
		self.set_point = set_point
		self.Integrator=0
		self.Derivator=0

	def setIntegrator(self, Integrator):
		self.Integrator = Integrator

	def setDerivator(self, Derivator):
		self.Derivator = Derivator

	def setKp(self,P):
		self.Kp=P

	def setKi(self,I):
		self.Ki=I

	def setKd(self,D):
		self.Kd=D

	def getPoint(self):
		return self.set_point

	def getError(self):
		return self.error

	def getIntegrator(self):
		return self.Integrator

	def getDerivator(self):
		return self.Derivator


def onpress(event):
	global A, B, C
	pl.clf()

	print "Pressed: ", event.key
	if event.key == "r":
		A *= 1.1
	elif event.key == "f":
		A *= 0.9
	elif event.key == "t":
		B *= 1.1
	elif event.key == "g":
		B *= 0.9
	elif event.key == "y":
		C *= 1.1
	elif event.key == "h":
		C *= 0.9

	pid_x=PID(A, B, C)
	pid_y=PID(A, B, C)

	set_point_x = 1.0 # set point
	set_point_y = 1.0 # set point
	
	position_x = 0.0
	velocity_x = 0.0
	position_y = 0.0
	velocity_y = 0.0

	points_x, points_y = [], []
	target_x, target_y = [], []
	D = 500

		
	for i in xrange(D):

		if i % 50 == 0:
			set_point_x = random.random()
			set_point_y = random.random()
			
			pid_x.setPoint(set_point_x)
			pid_y.setPoint(set_point_y)	

		pid = pid_x.update(position_x)
		velocity_x = velocity_x + 0.1 * pid
		position_x = position_x + 0.1 * velocity_x

		pid = pid_y.update(position_y)
		velocity_y = velocity_y + 0.1 * pid
		position_y = position_y + 0.1 * velocity_y

		points_x.append(position_x)
		points_y.append(position_y)
		target_x.append(set_point_x)
		target_y.append(set_point_y)
		



	pl.title("P=%2.2f, I=%2.2f, D=%2.2f" % (A, B, C))
	pl.plot(points_x, ':r')
	pl.plot(points_y, ':b')
	pl.xlim([0, 500])
	pl.ylim([-2, 2])
	pl.draw()


fig = pl.figure()
cid = fig.canvas.mpl_connect('key_press_event', onpress)
pl.show()

# xdot = Ax + Bu


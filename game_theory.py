# Find mixed-strategy Nash equlibria in two player game. 

import numpy as np
import math
from sympy.solvers import solve
from sympy import Symbol

left = np.array([ [1, 1], [2, 2]])
top  = np.array([ [3, 4], [5, 6]])

class Player:

	def __init__(self, name, actions):

		self.name = name
		self.actions = actions

	def get_actions(self):

		return self.actions

	def action(self, k):

		return self.actions[k]

class Game:

	def __init__(self, p1, p2, payoffs):

		self.p1 = p1
		self.p2 = p2
		self.payoffs = payoffs

		print "Created game with 2 players."

	def get_payoff(self, p1_action, p2_action):

		return self.payoffs[(p1.action(p1_action),p2.action(p2_action))]

	def mixed_strategy_nash_equilibrium(self):

		# Find the strategy (probability distribution) that makes the other player indifferent
		q = Symbol('q')		
		eqn = self.get_payoff(0, 0)[1]*q + self.get_payoff(1, 0)[1]*(1-q) - self.get_payoff(0, 1)[1]*q -self.get_payoff(1, 1)[1]*(1-q) 
		print p1.name, "must play", [solve(eqn, q)[0], 1 - solve(eqn, q)[0]]

		# Find the strategy (probability distribution) that makes the other player indifferent
		p = Symbol('p')		
		eqn = self.get_payoff(0, 0)[0]*p + self.get_payoff(0, 1)[0]*(1-p) - self.get_payoff(1, 0)[0]*p -self.get_payoff(1, 1)[0]*(1-p) 
		print p2.name, "must play", [solve(eqn, p)[0], 1 - solve(eqn, p)[0]]
				
p1 = Player("Small Piggie", ['Press', 'Wait'])
p2 = Player("Large Piggie", ['Press', 'Wait'])

payoffs = {
	('Press', 'Press')   : (1, 5),
	('Press', 'Wait')  : (-1, 9),
	('Wait', 'Press')  : (4, 4),
	('Wait', 'Wait') : (0, 0),
}

g = Game(p1, p2, payoffs)
g.mixed_strategy_nash_equilibrium()

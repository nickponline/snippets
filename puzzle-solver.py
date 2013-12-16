import sys
import copy

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

class Piece:
	def __init__(self, rep, id):
		self.bits = []
		self.ids = []
		self.description = []
		self.id = id

		self.fromString(rep)

	def hmax(self):
		return max([x for (x,y) in self.bits])

	def vmax(self):
		return max([y for (x,y) in self.bits])

	def hmin(self):
		return min([x for (x,y) in self.bits])

	def vmin(self):
		return min([y for (x,y) in self.bits])


	def fromString(self, rep):
		rep = rep.split("\n")
		self.bits = []
		for y in xrange( len(rep) ):
			for x in xrange( len(rep[y]) ):
				if (rep[y][x] == '#'):
					self.bits.append((x,y))
					self.ids.append(self.id)

	def rotate(self):
		for i, (x, y) in enumerate(self.bits):
			self.bits[i] = (y, -x)

		xmin = self.hmin()
		ymin = self.vmin()


		for i, (x,y) in enumerate(self.bits):
			self.bits[i] = (x-xmin, y-ymin)


	def hflip(self):
		hmax = max([x for (x,y) in self.bits])
		for i, (x, y) in enumerate(self.bits):
			self.bits[i] = (hmax - x, y)

	def vflip(self):
		vmax = max([y for (x,y) in self.bits])
		for i, (x, y) in enumerate(self.bits):
			self.bits[i] = (x, vmax - y)
	
	def __repr__(self):
		hmax = max([x for (x,y) in self.bits])
		vmax = max([y for (x,y) in self.bits])
		rep = ""

		for y in xrange(vmax+1):
			for x in xrange(hmax+1):
				try:
					idx = self.bits.index((x,y))
					rep += str(self.ids[idx])
				except:
					rep += '.'
			rep += '\n'
		return rep


	def canFit(self, piece, offsetx, offsety):
		possible = True
		hmax = max([x for (x,y) in self.bits])
		vmax = max([y for (x,y) in self.bits])
		
		for (x, y) in piece.bits:
			if  ((x + offsetx) > hmax) or ((y + offsety) > vmax):
				possible = False  
			try:
				idx = self.bits.index((offsetx+x, offsety+y))
				possible = False
			except:
				pass

		return possible

	def add(self, piece, offsetx, offsety):
		for (x, y) in piece.bits:
			self.bits.append((offsetx+x, offsety+y))
			self.ids.append(piece.id)
		
		
	def remove(self, piece, offsetx, offsety):
		for (x, y) in piece.bits:
			self.bits.remove((offsetx+x, offsety+y))
			self.ids.remove(piece.id)


	
def make_output(rs, fs):
	if fs == 0:
		return (rs)
	return (rs, 4)


def placePieces(remaining, board, solution):
	if remaining == []:
		print "Solution found:"
		# print board
		for i, x, y, (rs, fs) in solution:
			print i, x, y, make_output(rs, fs)
		
		return None

	#print board

	hmax = board.hmax()
	vmax = board.vmax()
	
	piece = remaining[0]

	for offsetx in xrange(hmax+1):
		for offsety in xrange(vmax+1):

			original = copy.deepcopy(remaining[0])
			
			for rotations in xrange(4):
				for flips in xrange(2):

					for r in xrange(rotations):
						original.rotate()
					for r in xrange(flips):
						original.hflip()


					if board.canFit(original, offsetx, offsety):
						board.add(original, offsetx, offsety)
						solution.append(((original.id, offsetx, offsety, (rotations, flips))))
						placePieces(remaining[1:], board, solution)
						solution.remove(((original.id, offsetx, offsety, (rotations, flips))))
						board.remove(original, offsetx, offsety)
						

boardRep = """###########
###    ## #
#         #
##       ##
#        ##
#         #
#        ##
#        ##
#         #
####   ####
###########"""

board = Piece(boardRep, 0)
print board


pieces = []

pieces.append(""" # ##
 ### 
#####
#####
# ## """)


pieces.append(""" ### 
#### 
 ### 
 ####
  ###""")
 
pieces.append(""" #  #
#####
 ### 
 ### 
 #   """)

pieces.append("""##   
 ####
#### 
#### 
#  # """)

for i in xrange(len(pieces)):
	pieces[i] = Piece(pieces[i], i+1)
	print pieces[i]

placePieces(pieces, board, [])

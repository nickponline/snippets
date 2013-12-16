# INOMCPLETE
# x0 = seed
# x = a*x + c mod m
# The period of a general LCG is at most m, and for some choices of a much less than that. Provided that c is nonzero, the LCG will have a full period for all seed values if and only if:[2]
#  and  are relatively prime,
#  is divisible by all prime factors of ,
#  is a multiple of 4 if  is a multiple of 4.

def isprime(n):
    '''check if integer n is a prime'''
    # make sure n is a positive integer
    n = abs(int(n))
    # 0 and 1 are not primes
    if n < 2:
        return False
    # 2 is the only even prime number
    if n == 2: 
        return True    
    # all other even numbers are not primes
    if not n & 1: 
        return False
    # range starts with 3 and only needs to go up the squareroot of n
    # for all odd numbers
    for x in range(3, int(n**0.5)+1, 2):
        if n % x == 0:
            return False
    return True


def nextinteger(X):
	X = (A*X + B) % (2 ** 64)
	return X

def nextinteger2(X):
	X = (A**V*X + (A ** V - 1) * (B / (A-1)))  % (2 ** 64)
	return X

X = 11413960417
A = 8433437992146984169
B = 0

for i in xrange(20):
	X = nextinteger(X)
	print X / (2 ** 56), ",",

print ""
X = 11413960417
A = 8433437992146984169
B = 0
	

for i in xrange(20):
	X = nextinteger2(X)
	print X / (2 ** 56), ",",


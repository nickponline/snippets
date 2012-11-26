"""
 Constrained multi-processor scheduling algorithm - BME 2009 EC Problem B
 Slow, will benefit from heaps
"""
class Course:
	pass

EOLN = "\n"

filename = "B/B5.in"
input_data = open(filename).read().strip().split(EOLN)

C, P, R, L = map(int, input_data[0].strip().split(" "))
courses = []

for line in input_data[1:]:
	line = map(int, line.strip().split(" "))
	id, length, lecturers = line[0], line[1], set(line[2:])
	course           = Course()
	course.id        = id
	course.length    = length
	course.lecturers = lecturers

	print course.id, course.length, course.lecturers
	courses.append(course)

rooms      = [0] * R
teacher    = [set()] * R


def allocate(rooms, teacher, courses, duration):
	# Allocate a course
	longest = -1
	best_course = None
	for course in courses:
		# Find an empty room
		if course.length > longest or longest == -1:
			for i in xrange(len(rooms)):
				if len(course.lecturers.intersection(teacher[i])) > 0:
					continue
				if (rooms[i] > 0):
					continue
				
				best_course = course
				longest = course.length 

	ret = True
	if not best_course:
		# print "No allocation possible", rooms
		ret = False

	else:
		for i in xrange(R):
			if rooms[i] == 0:
				rooms[i] = best_course.length
				teacher[i] = teacher[i].union(course.lecturers)
				# print "Allocating course ", best_course.id, " to room ", i
				# print "After allocating: ", rooms
				courses.remove(best_course)
				break

	return rooms, teacher, courses, ret

def free(rooms, teacher):
	shortest = 1000
	shortest_index = -1
	for i in xrange(len(rooms)):
		if rooms[i] < shortest:
			# print rooms
			# print "Bester room to free is", i, rooms[i]
			shortest = rooms[i]
			shortest_index = i

	
	teacher[shortest_index] = set()

	for i in xrange(len(rooms)):
		rooms[i] -= shortest

	# print "ROOMS AFTER FREE", rooms
	# print "After freeing:", rooms

	return rooms, teacher, shortest

duration = 0
while len(courses) > 0:

	
	rooms, teacher, courses, ret = allocate(rooms, teacher, courses, duration)
	if (ret):
		continue
	else:
		rooms, teacher, shortest = free(rooms, teacher)
		duration = duration + shortest
		print duration

max_duration = 0
for i in xrange( len(rooms) ):
	if rooms[i] > max_duration:
		max_duration = rooms[i]

duration = duration + max_duration

print "Total time taken: " , duration


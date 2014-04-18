# Justin Frye jmfrye
# 4-16-2014
# 15-221 Spring 2014
# intersect.py

import graph

def militaryTime(s):
	# e.g. s = 10:20AM
	AMorPM = s[-2:]
	(hour,minute) = s[:-2].split(":")
	(hour,minute) = (int(hour), int(minute))

	if (AMorPM == "AM"):
		return 60*(hour%12) + minute
	elif (AMorPM == "PM"):
		return 60*12 + 60*(hour%12) + minute

def testMilitaryTime():
	print "Testing militaryTime"
	assert(militaryTime("12:00AM") == 0)
	assert(militaryTime("12:01AM") == 1)
	assert(militaryTime("12:59AM") == 59)
	assert(militaryTime("1:01AM") == 61)
	assert(militaryTime("10:20AM") == 10*60 + 20)
	assert(militaryTime("12:00PM") == 60*12)
	assert(militaryTime("12:59PM") == 60*12 + 59)
	assert(militaryTime("11:59PM") == 60*23 + 59)
	print "PASSED! testMilitaryTime"

def intersect(start1,end1,day1,start2,end2,day2):

	# Check day intersect (e.g., day = "MWF" or day = "TR")
	sameDay = False
	day1 = graph.parseIntoArrayDays(day1)
	day2 = graph.parseIntoArrayDays(day2)
	for d in day1:
		if d in day2:
			sameDay = True

	if (sameDay == False):
		return False
	else:
		(s1,e1,s2,e2) = map(militaryTime, [start1, end1, start2, end2])
		# Check time intersect
		return ((s1 <= s2 and e1 >= s2) or 
				(s2 <= s1 and e2 >= s1))

def testIntersect():
	print "Testing intersect"
	assert(intersect("9:00AM","10:20AM","TR","10:30AM","12:20PM","MW") == False)
	assert(intersect("9:00AM","10:20AM","TR","10:30AM","12:20PM","TR") == False)
	assert(intersect("9:00AM","10:20AM","TR","9:00AM","12:20PM","TR") == True)
	assert(intersect("9:00AM","10:20AM","TR","8:00AM","9:20AM","TR") == True)
	assert(intersect("9:00AM","10:20AM","TR","8:00AM","9:20AM","T") == False)

	print "PASSED! testIntersect"

def testAll():
	testMilitaryTime()
	testIntersect()

#testAll()
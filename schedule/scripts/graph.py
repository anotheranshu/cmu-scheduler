import intersect
import getCourses


f = open('dict.txt', 'rb')

s =  eval(f.read())
#for key in s:
#	print key,s[key]

oguzList = [15210,15150,15122,15451]
graphDict = {}

#{CID: ARRAY OF POSTREQS}

def turnToString(cid):
	return str(cid)


def noPreReqs(cid,oguzList):
	cid = turnToString(cid)
	tempPrereq = s[cid][9] #9 is prereqs
	#print tempPrereq
	finalPrereq = getCourses.prereqs(tempPrereq)
	#print finalPrereq
	for possiblePreReq in oguzList:
		for course in finalPrereq:
			if isinstance(course,list):
				for inCourse in course:
					if inCourse == possiblePreReq:
						return False #found prereq
			else: #course
				if course == possiblePreReq:
					return False #found prereq
	return True

def militaryTime(s):
	# e.g. s = 10:20AM
	AMorPM = s[-2:]
	(hour,minute) = s[:-2].split(":")
	(hour,minute) = (int(hour), int(minute))

	if (AMorPM == "AM"):
		return 60*(hour%12) + minute
	elif (AMorPM == "PM"):
		return 60*12 + 60*(hour%12) + minute

def intersect(start1,end1,day1,start2,end2,day2):

	# Check day intersect (e.g., day = "MWF" or day = "TR")
	sameDay = False
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

def returnNoPreReqs(oguzList):
	allWithNoPreReqs = []
	for cid in oguzList:
		if noPreReqs(cid,oguzList):
			allWithNoPreReqs.append(cid)
	return allWithNoPreReqs

def parseIntoArrayDays(days):
	return days

#print parseIntoArrayDays("MTWTRF")

def updateDict(available,course):
	info = s[turnToString(course)]
	courseStart = info[7]
	courseEnd = info[8]
	courseDays = info[10]
	#print available
	for key in available:
		dayCourses = available[key]
		#print "available:",available
		for classInDay in dayCourses:
			startTime = classInDay[0]
			endTime = classInDay[1]
			#print startTime
			#print endTime
			#print classInDay
			if intersect(startTime,endTime,key,courseStart,courseEnd,courseDays):
				return available
	arrayDays = parseIntoArrayDays(courseDays)

	for day in arrayDays:
		dayCourses = available[day]
		dayCourses.append((courseStart,courseEnd,course))
		available[day] = dayCourses
	return available
	


def findUnits():
	neededCourses = returnNoPreReqs(oguzList)
	currentHours = 0
	available = {"M": [], "T": [], "W":[], "R":[], "F":[]}
	thresholdHrs = 60
	#print neededCourses
	for course in neededCourses:
		#print course
		currCourseHrs = s[turnToString(course)][1]
		if ((currCourseHrs+currentHours) <= thresholdHrs):
			available = updateDict(available,course)
			currentHours = currentHours + currCourseHrs
		#print available
	return available


#returnNoPreReqs(oguzList)
findUnits()
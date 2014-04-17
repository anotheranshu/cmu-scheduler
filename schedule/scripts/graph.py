import getCourses


f = open('dict.txt', 'rb')

s =  eval(f.read())
#for key in s:
#	print key,s[key]

oguzList = [15210,15150,15122,15451,15112]
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


def returnNoPreReqs(oguzList):
	allWithNoPreReqs = []
	for cid in oguzList:
		if noPreReqs(cid,oguzList):
			allWithNoPreReqs.append(cid)
	print allWithNoPreReqs

def parseIntoArrayDays(days):
	l = len(days)
	i = 0
	result = []
	while i < l:
		if days[i] == "M":
			result.append("M")
		elif days[i] == "T":
			if (i+1 < l) and (days[i+1] == "R"):
				result.append("TR")
			else:
				result.append("T")
		elif days[i] == "W":
			result.append("W")
		elif days[i] == "F":
			result.append("F")
		i = i + 1
	return result

print parseIntoArrayDays("MTWTRF")

def updateDict(available,course):
	info = s[turnToString(course)]
	courseStart = info[7]
	courseEnd = info[8]
	courseDays = info[10]
	for key in available:
		dayCourses = available[key]
		for classInDay in dayCourses:
			startTime = dayCourses[0]
			endTime = dayCourses[1]
			if intersect(startTime,endTime,key,courseStart,courseEnd,courseDays):
				return {}
	arrayDays = parseIntoArrayDays(courseDays)
	for day in arrayDays:
		dayCourses = available[day]
		dayCourses.append((courseStart,courseEnd))
		available[day] = dayCourses
	return available
	


def findUnits():
	neededCourses = returnNoPreReqs(oguzList)
	currentHours = 0
	available = {"M": [], "T": [], "W":[], "TR":[], "F":[]}
	thresholdHrs = 60
	for course in neededCourses:
		currCourseHrs = s[turnToString(course)][1]
		if ((currCourseHrs+currentHours) <= thresholdHrs):
			if updateDict(available,course) == {}:
				continue
			else:
				available = updateDict(available,course)
				currentHours = currentHours + currCourseHrs


returnNoPreReqs(oguzList)
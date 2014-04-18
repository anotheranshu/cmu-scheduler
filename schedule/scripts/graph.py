import intersect
import getCourses
import cs_course_giver

f = open('dict.txt', 'rb')

s =  eval(f.read())
#for key in s:
#	print key,s[key]

#oguzList = cs_course_giver.giveCoursesForUser("user","pw")
oguzList = [15451, 15128, 15453, 15317, 15410, 15291, 1620, 88205, 79207, 79226]
#print oguzList
graphDict = {}

#{CID: ARRAY OF POSTREQS}

def turnToString(cid):
	return str(cid)


def noPreReqs(cid,oguzList):
	cid = turnToString(cid)
	if cid not in s:
		return True
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
	if turnToString(course) not in s:
		return available
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
	


def findUnits(oguzList):
	neededCourses = returnNoPreReqs(oguzList)
	currentHours = 0
	available = {"M": [], "T": [], "W":[], "R":[], "F":[]}
	thresholdHrs = 35
	#print neededCourses
	for course in neededCourses:

		if turnToString(course) not in s:
			currCourseHrs = 9
		else:
			currCourseHrs = s[turnToString(course)][1]
		if ((currCourseHrs+currentHours) <= thresholdHrs):
			available = updateDict(available,course)
			currentHours = currentHours + currCourseHrs
		#print available
	return available

def extractCourses(available):
	currCourses = set()
	for day,value in available.items():
		for tup in value:
			course = tup[2]
			currCourses.add(course)
	return currCourses

def restSchedule():
	remainingCourses = oguzList
	i = 0
	allSchedule = []
	while len(remainingCourses) != 0:
		available = findUnits(remainingCourses)
		humanities = set()
		for course in remainingCourses:
			#find random not cs course and add
			string = str(course)
			if string[:-3] != "15": #cs
				humanities.add(course)
				remainingCourses.remove(course)
				break;

		allSchedule.append(extractCourses(available) | humanities)
		currCourses = extractCourses(available)
		oguzSet = set(remainingCourses)
		remainingCourses = list(oguzSet.difference(currCourses))
	print allSchedule

restSchedule()
#returnNoPreReqs(oguzList)
#findUnits()
# restSchedule(oguzList)

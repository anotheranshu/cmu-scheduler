import apis

f = open('schedule.txt', 'rb')

def isValidRow(infoList):

	if len(infoList) < 10:
		return False
	#print infoList[4]
	#print len(infoList[4])
	if (not infoList[0].isdigit()):
		return False
	elif (infoList[4] == "TBA"): #no schedule time for course
		return False
	elif infoList[0].strip() == '': #no course id (recitation)
		return False   #MAY CHANGE TO TRUE LATER (consider recitation)
	#elif (not infoList[0][0:2] == "15"): # not CS class
	#	return False
	else:
		return True

def scheduleTimes(courseDict):
	i = 0
	for line in f :
		infoList = line.split('\t')
		if not isValidRow(infoList):
			continue
		#print infoList
		#typeOfClass = 
		cid = infoList[0]
		units = infoList[2]
		startTime = infoList[5]
		endTime = infoList[6]
		#print cid,units,startTime,endTime
		if cid in courseDict: #will only work for CS classes
			currCourse = courseDict[cid]
			#name,hrsperweek,numratings,course rating,professor,
			#description, units, startTime, endTime
			currCourse[6] = units
			currCourse[7] = startTime
			currCourse[8] = endTime
			courseDict[cid] = currCourse

		i = i +1 
		#if (i > 100):
		#	break
	return courseDict


import csv
import json
from pprint import pprint

class Class(object):
	def __init__(self,cid,course_name,hrsPerWeek,numRatings,course_rating,professors,description):
		self.cid = cid
		self.course_name = course_name
		self.numRatings = numRatings
		self.hrsPerWeek = hrsPerWeek
		self.course_rating = course_rating
		self.professors = professors
		self.description = description

def updateDict(temp_scs_courses,row):
	professor = row[2][1:]
	cid = (row[5])
	course_name = row[6]
	hrsPerWeek = float(row[12])
	course_rating = float(row[20])
	#cid maps to [course_name,hrs,numRatings,avgRating,professorDict(numRating,avg)]
	if cid in temp_scs_courses.keys():
		currClass = temp_scs_courses[cid]		
		currNumRating = currClass[2] #might have to check if int
		currAvgRating = currClass[3]
		currAvgRating = (currNumRating*currAvgRating + course_rating)/(currNumRating+1)
		currHrsPerWeek = (currNumRating*currClass[1] + hrsPerWeek)/(currNumRating+1)
		classProfessors = currClass[4] #(avgRating,num)
		if professor in classProfessors:
			currProfessor = classProfessors[professor]
			currProfessorNumRating = currProfessor[1]
			currProfessorAvgRating = (currProfessorNumRating*currProfessor[0]
								 + course_rating)/ (currProfessorNumRating+1)
			classProfessors[professor] = (currProfessorAvgRating,currProfessorNumRating+1)
			currProfessorNumRating = currProfessorNumRating+1

		else:
			classProfessors[professor] = (course_rating,1)
		updateInfo = [currClass[0],currHrsPerWeek,currNumRating+1,
					  currAvgRating,classProfessors,""]
		temp_scs_courses[cid] = updateInfo
	else:
		temp = [course_name,hrsPerWeek,1,course_rating
				,{professor:(course_rating,1)},""]
		temp_scs_courses[cid] = temp
	return temp_scs_courses

#checks if row is valid
def isValidRow(row):
	cid = row[5]
	course_rating = row[20]
	if (not cid.isdigit()) or (course_rating == ""):
		return False
	return True

def readSCSFCE():
	with open('SurveyResults-SchoolComputerScience-allyears.csv', 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		i = 0
		temp_scs_courses = {}
		scs_courses = []
		json_scs_courses = []
		for row in spamreader:
			if i < 5: #first 5 rows for SCS is headers and stuff
				i = i + 1
				continue
			if (not isValidRow(row)): #might need to work more on this!
				continue
			temp_scs_courses = updateDict(temp_scs_courses,row)
			if (i>= 1000):
				break
			i = i + 1
		return temp_scs_courses
		for key,value in temp_scs_courses.items():
			cid = key
			course_name = value[0]
			hrsPerWeek = value[1]
			numRatings = value[2]
			course_rating = value[3]
			professors = value[4]
			newCourse = Class(cid,course_name,hrsPerWeek,numRatings,
								course_rating,professors)
			#scs_courses.append(newCourse)
			#json_scs_courses.append(json.dumps(vars(newCourse),sort_keys=True, indent=4))
		#for currCourse in json_scs_courses:
		#	print currCourse
		#return scs_courses


def parseJson():
	#json_data=open('courses.json','rb')
	#result = json_data.read()
	#print result
	#print json.loads(result)
	courseDict = readSCSFCE()
	with open('courses2.json') as json_data:
		d = json.load(json_data)
    	json_data.close()
    	#pprint(d)
	
	for course in d:
		cid = course['courseId']
		if cid in courseDict:
			currCourse = courseDict[cid]
			currCourse[5] = course['description']
			#print currCourse[5]
			courseDict[cid] = currCourse
		else:
			continue
		#print courseDict
	json_scs_courses = []
	for key,value in courseDict.items():
		cid = key
		course_name = value[0]
		hrsPerWeek = value[1]
		numRatings = value[2]
		course_rating = value[3]
		professors = value[4]
		description = value[5]
		newCourse = Class(cid,course_name,hrsPerWeek,numRatings,
							course_rating,professors,description)
		#scs_courses.append(newCourse)
		json_scs_courses.append(json.dumps(vars(newCourse),sort_keys=True, indent=4))
	for currCourse in json_scs_courses:
		print currCourse
	#jsonFormat = result[1:-2]
	#print jsonFormat
	#print json.dumps(result,sort_keys=True,indent=4)
	#data = json.load(json1)
	#pprint(data)

parseJson()
#readSCSFCE()

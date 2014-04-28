from lxml import html
import requests
from django.conf import settings

f = open(settings.PROJECT_PATH + "/schedule/scripts/dict.txt", 'rb')

s =  eval(f.read())

def getCourseDescriptionPreReqs(cid,semester):
	title = ""
	if semester == "F14":
		fileRead = open('schedule.txt', 'rb')
	else:
		fileRead = open('scheduleSpring.txt','rb')
	for line in fileRead:
		infoList = line.split('\t')
		if cid == infoList[0]:
			title = infoList[1]
	if cid in s:
		hrsPerWeek = s[cid][1]
	else:
		hrsPerWeek = None
	try:
		url = 'https://enr-apps.as.cmu.edu/open/SOC/SOCServlet/courseDetails?COURSE=%s&SEMESTER=%s' % (cid,semester)
		page = requests.get(url) 
		tree = html.fromstring(page.text)
		description = tree.xpath('//*[@id="course-detail-description"]/p/text()')[0]
		return [description,hrsPerWeek,title]
	except:
		#print "Class not available for Fall 2014"
		return ["",hrsPerWeek,title]

def getCourseInfo(cid):
	[descriptionF,hrsPerWeekF,titleF] = getCourseDescriptionPreReqs(cid,"F14")
	if descriptionF == "": #try spring 2014
		return getCourseDescriptionPreReqs(cid,"S14")
	else:
		return [descriptionF,hrsPerWeekF,titleF]

#getCourseInfo("15150")

from lxml import html
import requests



def getCourseDescriptionPreReqs(cid,semester):
	try:
		url = 'https://enr-apps.as.cmu.edu/open/SOC/SOCServlet/courseDetails?COURSE=%s&SEMESTER=%s' % (cid,semester)
		page = requests.get(url) 
		tree = html.fromstring(page.text)
		description = tree.xpath('//*[@id="course-detail-description"]/p/text()')[0]
		prereqs = tree.xpath('//*[@id="course-detail-modal-body"]/div[4]/div[1]/dl/dd/text()')[0]
		#units = tree.xpath('//*[@id="course-detail-modal-body"]/div[1]/div/table/tr[1]/text()')
		units = tree.xpath('//tr[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]//td[(((count(preceding-sibling::*) + 1) = 2) and parent::*)]/text()')[0]
		#print description
		#print prereqs
		return [description,prereqs,units]
	except:
		#print "Class not available for Fall 2014"
		return ["","",""]


getCourseDescriptionPreReqs("15150","F14")

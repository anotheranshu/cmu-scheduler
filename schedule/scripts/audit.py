from pyquery import PyQuery as pq
from sets import Set
from authenticate import authenticate
from datetime import datetime
from urllib import urlencode
from icalendar import Calendar, Event, UTC
import re
import json

class AuthenticationError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)


#returns true if authentication successful, else false
def isAuthenticated():
    try:
        s = authenticate('https://enr-apps.as.cmu.edu/audit/audit')
        return True;
    except KeyError:
        return False;

def get_all_courses():
    ''' extracts your grades from CMU's academic audit
    returns a json of course -> letter grade (string)
    * means you're taking the class and grades haven't been put in yet
    AP means you got it through AP credit
    P is pass
    '''
    if (not isAuthenticated()):
        print "Authentication Failed"
        return

    s = authenticate('https://enr-apps.as.cmu.edu/audit/audit')

    # find out the params for main major auditing
    mainFrame = s.get('https://enr-apps.as.cmu.edu/audit/audit?call=2').content

    d = pq(mainFrame)
    params = {'call': 7}
    for htmlInput in d('input[type=hidden]'):
        name = d(htmlInput).attr('name')
        value = d(htmlInput).attr('value')
        if name != 'call':
            params[name] = value

    # get page for given major
    classes = s.get('https://enr-apps.as.cmu.edu/audit/audit?' + urlencode(params)).content
    
    # take grades from <pre>s in the page
    d = pq(classes)
    major_courses = Set([])
    all_courses = Set([])
    for pre in d('pre'):
        data = d(pre).text()
        for line in data.split('\n'):
            matches = re.search('(\d+-\d+) \w+\s*\'\d+ ((\w|\*)+)\s*(\d+\.\d)\s*$', line)
            if matches is not None:
                major_course = matches.group(1)
                major_courses.add(major_course)
                all_courses.add(major_course)
            else:
            	nonmajor_course = re.search('(\d+-\d+) \w+\s*\'\d+ ((\w|\*)+)\s*(\d+\.\d)\s*', line)
            	if nonmajor_course is not None:
            		course = nonmajor_course.group(1)
            		all_courses.add(course)

                    
    print major_courses
    print all_courses
    return major_courses

get_all_courses()
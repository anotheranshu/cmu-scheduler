from pyquery import PyQuery as pq
from sets import Set
from authenticate import authenticate
from datetime import datetime
from urllib import urlencode
import re
import json

class AuthenticationError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)


#returns true if authentication successful, else false
def isAuthenticated(username,pw):
    try:
        s = authenticate('https://enr-apps.as.cmu.edu/audit/audit',username,pw)
        return True;
    except KeyError:
        return False;

def get_all_courses(username,pw):
    ''' extracts your grades from CMU's academic audit
    returns a json of course -> letter grade (string)
    * means you're taking the class and grades haven't been put in yet
    AP means you got it through AP credit
    P is pass
    '''
    if (not isAuthenticated(username,pw)):
        print "Authentication Failed"
        return

    s = authenticate('https://enr-apps.as.cmu.edu/audit/audit',username,pw)

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
    classlevel = ""
    major = -1
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
                else:
                    classLevelArray = line.split("CLASSLEVEL:")
                    if len(classLevelArray) > 1: #found class level
                        classlevel = classLevelArray[1]

    majorfile =  params['MajorFile']
    i = majorfile.find("SCS") 
    j = majorfile.find("ECE") #might need to change later?
    if i != -1:
        major = 0 # CS major
    elif j != -1:
        major = 1

    #print major_courses
    print all_courses
    print classlevel
    print major
    return [major_courses,classlevel,major]
    #semesters left and major

get_all_courses("USERNAME","PW")
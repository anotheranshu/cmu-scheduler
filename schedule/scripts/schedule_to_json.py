import json
import graph
import cs_course_giver
import infoForJson

# Requires: 2d array of courses
def getJsonVals(courses):
    semesters = ["Fall'14", "Spring'15", "Fall'15", "Spring'16", "Fall'16", "Spring'17", "Fall'17", "Spring'18"]

    result = []
    for year in xrange(len(courses)):
        preres = []
        for elem in courses[year]:
            (des, hrs, name) = infoForJson.getCourseInfo(str(elem))
            preres += [{"name": str(elem) + " - " + name, "children" : [{"name" : "Hours per week: " + str(hrs) + " -- Description: " + des, "size": 3938}]}]

        result += [{"name" : semesters[year], "children" : preres, "size": 3938}]

    return json.dumps({"name" : "schedule", "children" : result}, \
                      sort_keys=False, indent=4, separators=(',', ': '))

# For major
# 0 = CS
# 1 = ECE
def getJson(USERNAME, PASSWORD, major, wanted=[]):
    courses = cs_course_giver.giveCoursesForUser(USERNAME, PASSWORD, major, wanted)
    # courses = [15214, 15453, 15317, 15410, 15291, 1620, 88205, 79207, 79226]
    thresholdHrs = 60
    #f = open('flare.json', 'w')
    # print courses
    # print graph.restSchedule(courses, thresholdHrs)
    # print infoForJson.getCourseInfo("15411")

    s = getJsonVals(map (lambda x : list(x), graph.restSchedule(courses, thresholdHrs)))
    #f.write(s)
    # print s
    return s


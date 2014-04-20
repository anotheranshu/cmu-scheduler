import json
import graph
import cs_course_giver

# Requires: 2d array of courses
def getJsonVals(courses):
    result = []
    for year in xrange(len(courses)):
        result += [{"name" : str(year), \
        "children" : [{"name": str(elem), "size": 3938} \
        for elem in courses[year]]}]

    return json.dumps({"name" : "schedule", "children" : result}, \
                      sort_keys=False, indent=4, separators=(',', ': '))

def getJson(USERNAME, PASSWORD):
    courses = cs_course_giver.giveCoursesForUser(USERNAME, PASSWORD)
    thresholdHrs = 35
    f = open('flare.json', 'w')
    s = getJsonVals(map (lambda x : list(x), graph.restSchedule(courses, thresholdHrs)))
    f.write(s)
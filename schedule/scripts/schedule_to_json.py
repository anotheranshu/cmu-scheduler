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
    #courses = [15128, 15451, 15455, 15317, 15410, 15312, 9221, 80135, 79222, 80253]
    #print courses
    thresholdHrs = 35
    f = open('flare.json', 'w')
    print graph.restSchedule(courses, thresholdHrs)
    s = getJsonVals(map (lambda x : list(x), graph.restSchedule(courses, thresholdHrs)))
    f.write(s)





#[15128, 15451, 21301, 80311, 15440, 15237, 1201, 88110, 80100, 79241]




































getJson("sajidurr","PASSWORD")
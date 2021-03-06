import random
import audit

cs_courses = [
# CS Courses
({15122, 15150, 15210, 15213, 15251, 15451}, 6),
({15221}, 1),
({15354, 15355, 15453, 15455, 21301, 21484}, 1),
({2450, 5391, 5431, 10601, 11411, 15313, 15322, 15323, 15381, 15415, 15462, 16384, 16385}, 1),
({15312, 15317, 15414, 15424, 21300, 80311}, 1),
({15410, 15411, 15418, 15440, 15441}, 1),
({15322, 15214, 15237, 15239, 15291, 15295, 15312, 15313, 15317, 15319},2),

# Mathematics
({21120, 21122, 21127}, 3),
({21241, 21242}, 1),
({15359, 21325, 36217, 36225}, 1),

# Science and Engineering
({02261, 03124, 9101, 9221, 15321, 27100, 33104, 27100, 33104, 42203, 85310}, 1),
({42101, 9105, 9106, 12100, 18100, 24101, 33106, 33107, 33111, 33112, 3121}, 3),

# Humanities
({76101}, 1),
({70311, 80130, 80150, 80180, 80221, 80230, 80241, 80275, 80281, 85102, 85211, 85221, 85241, 85251, 85261, 85261, 88120, 88260}, 2),
({19101, 36303, 70332, 73100, 73230, 73240, 79331, 79335, 80135, 80136, 80235, 80244, 80245, 80341, 88104, 88110, 88205, 88220, 88326}, 2),
({57173, 60205, 70342, 76227, 76232, 76239, 76241, 79104, 79207, 79222, 79226, 79230, 79240, 79241, 79242, 79255, 79261, 79281, 79311, 79345, 79350, 79368, 80100, 80250, 80251, 80253, 80254, 80255, 80261, 80276, 82273, 82293, 82303, 82304, 82333, 82342, 82343, 82344, 82345}, 2)
]

def createAPool(taken, requirements, wanted = []):
    # a fix for ECE students
    if 18213 in taken:
        taken.add(15213)
    # a fix for CS students
    if 15151 in taken:
        taken.add(21127)

    result = wanted
    taken |= set(wanted)
    for (elem, num) in requirements:
        inter = taken.intersection(elem)
        if (num - len(inter) > 0):
            newL = list(elem - taken)
            result += random.sample(elem - taken, num - len(inter))
    return result

def giveCoursesForUser(USERNAME, PASSWORD, major, wanted = []):
    courses_taken = set(audit.get_all_courses(USERNAME, PASSWORD)[0])
    return createAPool(courses_taken, cs_courses, wanted)

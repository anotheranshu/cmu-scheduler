from django.db import models
from django.contrib.auth.models import User
from schedule.models import *
from django.utils import timezone
import datetime
import random
from django.conf import settings
import json
from pprint import pprint
import scripts.audit

DAILY_SUBMISSION_MAX = 5
PROBLEM_VALUE = 5
ACTIVITY_VALUE = 1
GROUP_SIZE = 4

def i_list_to_CSL(l):
  if len(l) == 0:
    return ""
  return (",".join(map(lambda n: str(n), l)))

def diff(a, b):
  b = set(b)
  return [aa for aa in a if aa not in b]

def coursenum_to_id(n):
  return Course.objects.get(course_num=n).node_id

#Creates a new student with the given parameters and saves them to the database (with a User for them)
def make_student(myandrew, mypassword):
  u = User.objects.create_user(myandrew, (myandrew + "@andrew.cmu.edu"), myandrew, first_name=myandrew, last_name=myandrew)
  student_data = audit.get_all_courses(myandrew, mypassword)
  mycourses = map(lambda n: coursenum_to_id(n), student_data[0])
  mysems_left = 6
  if (student_data[1] == "Sophomore"):
    sems_left = 4
  elif (student_data[1] == "Junior"):
    sems_left = 2
  else:
    pass
  myis_cs = (not bool(student_data[2]))
  student = Student(user=u, andrew=myandrew, taken_courses=mycourses, sems_left=mysems_left, is_cs=myis_cs)
  student.save()
  return student

def import_courses():
  raw_json = (open(settings.PROJECT_PATH + "/schedule/static/data/courses.json")).read()
  data = json.loads(raw_json)
  for course in data:
    mydescription = course.get("description", "")
    mytitle = course.get("title", "")  
    myid = course.get("courseId", "")
    mytree = course.get("treeType", "")
    mystarter = course.get("isStarter", False)
    myprereq_indices = i_list_to_CSL(course.get("prereqIndices", ""))
    mypostreq_indices = i_list_to_CSL(course.get("postreqIndices", ""))
    mynodeid = course["nodeId"] # We *should* fail if there's no node ID.  There is no default value for this.
    dcourse = Course(course_id=myid, tree_type=mytree, is_starter=mystarter, prereq_indices=myprereq_indices, postreq_indices=mypostreq_indices, description=mydescription, node_id=mynodeid, title=mytitle)
    dcourse.save()

  for course in Course.objects.all():
    print course
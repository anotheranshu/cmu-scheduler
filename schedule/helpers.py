from django.db import models
from django.contrib.auth.models import User
from schedule.models import *
from django.utils import timezone
import datetime
import random
from django.conf import settings
import json

DAILY_SUBMISSION_MAX = 5
PROBLEM_VALUE = 5
ACTIVITY_VALUE = 1
GROUP_SIZE = 4

def diff(a, b):
	b = set(b)
	return [aa for aa in a if aa not in b]

def current_problems(student):
	return diff(problem_field_to_list(student.group.discovered_problems), problem_field_to_list(student.group.solved_problems))

def current_activities(student):
	return diff(problem_field_to_list(student.group.discovered_activities), problem_field_to_list(student.group.solved_activities))

def make_problem(title, lead_text, filename, answer, associated_instructor=""):
	problem = Problem(title=title, answer=answer, instructor=associated_instructor, file_name=filename, lead_text=lead_text)
	problem.save()

def make_activity(title, lead_text, filename, associated_instructor=""):
	activity = Activity(title=title, lead_text=lead_text, file_name=filename, instructor=associated_instructor)
	activity.save()
	L = Problem.objects.filter(instructor__iexact=associated_instructor)
	for p in list(L):
		p.activity = activity
		p.save()
	activity.save()

def make_problem_from_file(filename):
	f = open(filename)
	title = f.readline().strip()
	lead_text = f.readline().strip()
	file_name = f.readline().strip()
	answer = f.readline().strip()
	associated_instructor = f.readline().strip()
	make_problem(title, lead_text, file_name, answer, associated_instructor)
	f.close()

def make_activity_from_file(filename):
	f = open(filename)
	title = f.readline().strip()
	lead_text = f.readline().strip()
	file_name = f.readline().strip()
	associated_instructor = f.readline().strip()
	make_activity(title, lead_text, file_name, associated_instructor)
	f.close()

#Creates a new student with the given parameters and saves them to the database (with a User for them)
def make_student(myandrew, myfname, mylname, mypassword=""):
	passwd = ""
	if (mypassword == ""):
		passwd = myandrew
	else:
		passwd = mypassword
	u = User.objects.create_user(myandrew, (myandrew + "@andrew.cmu.edu"), passwd, first_name = myfname, last_name = mylname)
	student = Student(user=u, andrew=myandrew, fname=myfname, lname=mylname)
	student.save()
	return student

def make_instructor(myandrew, myfname, mylname, mypassword=""):
	passwd = ""
	if (mypassword == ""):
		passwd = myandrew
	else:
		passwd = mypassword
	u = User.objects.create_user(myandrew, (myandrew + "@andrew.cmu.edu"), passwd, first_name = myfname, last_name = mylname)
	student = Student(user=u, andrew=myandrew, fname=myfname, lname=mylname)
	student.is_instructor = True
	student.save()
	return student

#Creates a new group with the given name and puts the students in it.  Currently does no checks for
#students already being in a group, student progress, etc.  Maybe a TODO.
def make_group(student_list, group_name=""):
	if (group_name == ""):
		group_name = " - ".join(map(lambda x: x.andrew, student_list))
	newgroup = StudentGroup(name=group_name)
	newgroup.save()
	for x in student_list:
		x.group = newgroup
		x.save()
	newgroup.save()
	return newgroup

#Regroups all students into new groups.  Does no checks.
def group_students():
	students = list(Student.objects.all())
	random.shuffle(students)
	lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
	for i, l in enumerate(lol(students, GROUP_SIZE)):
		g = make_group(l, "Group" + str(i))
		print(g.name)

'''Creates the class from the given roster, where each line is of the format:
<andrew> <fname> <lname> <password>
	and then puts the students into groups.  The entire class is regrouped.'''
def populate_students(filename):
	f = open(filename, 'r')
	for line in f:
		strs = line.split()
		s = make_student(strs[0], strs[1], strs[2], strs[3])
		print(s.fname)
	f.close()
	group_students()

def populate_students_csv(filename):
	f = open(filename, 'r')
	for line in f:
		strs = line.split(",")
		s = make_student(strs[0], strs[1], "", strs[3].strip())
		s.save()
		sg = StudentGroup.objects.filter(name=strs[2])
		if (len(sg) == 0):
			g = StudentGroup(name=strs[2])
			g.save()
			s.group = g
			s.save()
		else:
			s.group = sg[0]
			s.save()
	f.close()

def populate_instructors(filename):
	f = open(filename, 'r')
	for line in f:
		strs = line.split()
		s = make_instructor(strs[0], strs[1], strs[2], strs[3])
		print(s.fname)
	f.close()

def has_problem_access(student, problem_num):
	if (problem_num < 10):
		return (problem_num in problem_field_to_list(student.group.discovered_problems))
	else:
		return (len(problem_field_to_list(student.group.solved_activities)) == 7)

def has_activity_access(student, activity_num):
	return (activity_num in problem_field_to_list(student.group.discovered_activities))

def discover_problem(problem_num, student):
	if not has_problem_access(student, problem_num):
		student.group.discovered_problems = student.group.discovered_problems + " " + str(problem_num)
		student.group.save()

def discover_activity(activity, student):
	if activity is None:
		return
	if not has_activity_access(student, activity.id):
		student.group.discovered_activities = student.group.discovered_activities + " " + str(activity.id)
		student.group.save()


#Accepts a submission (student, answer, problem_number), checks the answer with the student's group's
#parameters, and puts the response into the database.  Returns 1 if the answer is correct, 0 if it is
#incorrect, and 2 if they hit they exceeded the maximum number of submissions.
def process_submission(student, answer, problem_number):
	retval = 0
	correct = False
	relevant_subs = filter(lambda x: x.timestamp.date() == timezone.now().date(), ProblemSubmission.objects.filter(studentgroup=student.group, problem_id=problem_number))
	if (((len(relevant_subs) >= DAILY_SUBMISSION_MAX) and (problem_number != 8) and (problem_number != 9)) or ((len(relevant_subs) >= 3) and problem_number == 10)):
		retval = 2 # Too many answers for one day (brute force suspected)
	elif (checkanswers(student, answer, problem_number)):
		retval = 1 # Correct
		correct = True
		if not student.group is None:
			for s in student.group.student_set.all():
				if ((not s.has_solved_problem(problem_number)) and s.track_group_problems):
					s.solved_problems = (s.solved_problems + " " + str(problem_number))
					s.problem_score = s.problem_score + PROBLEM_VALUE
					s.save()
			if (not student.group.has_solved_problem(problem_number)):
				student.group.solved_problems = (student.group.solved_problems + " " + str(problem_number))
				student.group.save()
		else:
			if (not student.has_solved_problem(problem_number)):
					student.solved_problems = (student.solved_problems + " " + str(problem_number))
					student.problem_score = student.problem_score + PROBLEM_VALUE
					student.save()
	else:
		retval = 0 # Incorrect or other
	sub = ProblemSubmission(student=student, studentgroup=student.group, problem=Problem.objects.get(pk=problem_number), correct=correct, answer=answer)
	sub.save()
	if correct:
		#Find the appropriate Activity and give access to that.
		activity = Problem.objects.get(pk=problem_number).activity
		discover_activity(activity, student)
		if (problem_number == 8):
			discover_problem(9, student)
		if (problem_number == 9):
			for i in range(1, 8):
				discover_problem(i, student)
	return retval

def checkanswers(student, answer, problem_number):
	return (answer == Problem.objects.get(pk=problem_number).answer)


def process_checkin(student_andrew, activity_num):
	student_group = Student.objects.get(andrew__iexact=student_andrew).group
	for s in student_group.student_set.all():
		if not s.has_solved_activity(activity_num):
			s.solved_activities = s.solved_activities + " " + str(activity_num)
			s.activity_score = s.activity_score + ACTIVITY_VALUE
			s.save()
			finished = True
			for i in range(1, 7):
				finished = (finished and s.has_solved_activity(i))
			if finished:
				discover_problem(10, s)
	if not student_group.has_solved_activity(activity_num):
		student_group.solved_activities = student_group.solved_activities + " " + str(activity_num)
	student_group.save()
	sub = ActivitySubmission(studentgroup=student_group, activity=Activity.objects.get(pk=activity_num))
	sub.save()


def setup_test_env():
	populate_students("/home/anshu/Development/puzzle_hunt/puzzlehunt/puzzle/static/roster.txt")
	populate_instructors("/home/anshu/Development/puzzle_hunt/puzzlehunt/puzzle/static/instructor_roster.txt")
	for i in range(1, 8):
		make_problem_from_file("/home/anshu/Documents/problem/" + str(i) + ".txt")
	for i in range(1, 8):
		make_activity_from_file("/home/anshu/Documents/activities/" + str(i) + ".txt")

	make_problem_from_file("/home/anshu/Documents/problem/owl.txt")
	make_problem_from_file("/home/anshu/Documents/problem/mum.txt")
	for g in StudentGroup.objects.all():
		g.discovered_problems = "8"
		g.save()

def setup_dev_env():
	print(settings.PROJECT_PATH)
	populate_students_csv(settings.PROJECT_PATH + "/puzzle/static/auxfiles/student_roster.txt")
	populate_instructors(settings.PROJECT_PATH + "/puzzle/static/auxfiles/instructor_roster.txt")
	for i in range(1, 8):
		make_problem_from_file(settings.PROJECT_PATH + "/puzzle/static/auxfiles/problem/" + str(i) + ".txt")
	for i in range(1, 8):
		make_activity_from_file(settings.PROJECT_PATH + "/puzzle/static/auxfiles/activities/" + str(i) + ".txt")
	make_problem_from_file(settings.PROJECT_PATH + "/puzzle/static/auxfiles/problem/owl.txt")
	make_problem_from_file(settings.PROJECT_PATH + "/puzzle/static/auxfiles/problem/mum.txt")
	for g in StudentGroup.objects.all():
		g.discovered_problems = "8"
		g.save()

def make_test_student(andrew, fname, lname, passwd):
	s = make_student(andrew, fname, lname, passwd)
	group = StudentGroup(name=("Test " + andrew), discovered_problems="8", tags="test")
	group.save()
	s.group = group
	s.save()
	group.save()

def make_guest_student(andrew, fname, lname, passwd):
	s = make_student(andrew, fname, lname, passwd)
	group = StudentGroup(name=("Guest " + andrew), discovered_problems="8", tags="guest")
	group.save()
	s.group = group
	s.save()
	group.save()

def make_TA_accounts():
	f = open(settings.PROJECT_PATH + "/puzzle/static/auxfiles/instructor_roster.txt", "r")
	for line in f:
		strs = line.split()
		make_test_student(strs[0].strip() + "-stu", strs[1].strip(), strs[2].strip(), strs[3].strip())
	f.close()

def retroactive_last_problem():
	make_problem_from_file(settings.PROJECT_PATH + "/puzzle/static/auxfiles/problem/final.txt")
	make_activity_from_file(settings.PROJECT_PATH + "/puzzle/static/auxfiles/activities/10.txt")
	for studentgroup in StudentGroup.objects.all():
		finished = True
		for i in range(1, 7):
			finished = (finished and studentgroup.has_solved_activity(i))
		if finished:
			studentgroup.discovered_problems = studentgroup.discovered_problems + " 10"
			studentgroup.save()

def import_courses():
	json.loads
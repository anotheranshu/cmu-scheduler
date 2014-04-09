from django.db import models
from django.contrib.auth.models import User

# Some helper functions.  Yeah, this is probably bad style.
def problem_field_to_list(myfield):
	return map(lambda x: int(x), myfield.split())

# Create your models here.

class StudentGroup(models.Model):
	name = models.CharField(max_length=100)
	tags = models.CharField(max_length=1000)
	discovered_problems = models.CharField(max_length=200)
	discovered_activities = models.CharField(max_length=200)
	solved_activities = models.CharField(max_length=200)
	solved_problems = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name
	def has_solved_problem(self, num):
		return (num in problem_field_to_list(self.solved_problems))
	def has_solved_activity(self, num):
		return (num in problem_field_to_list(self.solved_activities))

class Student(models.Model):
	is_instructor = models.BooleanField(default=False)
	user = models.OneToOneField(User)
	andrew = models.CharField(max_length=100)
	fname = models.CharField(max_length=100)
	lname = models.CharField(max_length=100)
	
	problem_score = models.IntegerField(default=0)
	activity_score = models.IntegerField(default=0)
	writeup_score = models.IntegerField(default=0)
	solved_problems = models.CharField(max_length=200)
	solved_activities = models.CharField(max_length=200)
	group = models.ForeignKey(StudentGroup, null=True, on_delete=models.SET_NULL)
	track_group_problems = models.BooleanField(default=True)
	def __unicode__(self):
		return self.andrew
	def has_solved_problem(self, num):
		return (num in problem_field_to_list(self.solved_problems))
	def has_solved_activity(self, num):
		return (num in problem_field_to_list(self.solved_activities))

class Activity(models.Model):
	title = models.CharField(max_length=500)
	lead_text = models.CharField(max_length=5000)
	file_name = models.CharField(max_length=100)
	instructor = models.CharField(max_length=100)

class Problem(models.Model):
	title = models.CharField(max_length=500)
	lead_text = models.CharField(max_length=5000)
	file_name = models.CharField(max_length=100)
	answer = models.CharField(max_length=10000)
	instructor = models.CharField(max_length=100)
	activity = models.ForeignKey(Activity, null=True, on_delete=models.SET_NULL)

class ProblemSubmission(models.Model):
	student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
	studentgroup = models.ForeignKey(StudentGroup, null=True, on_delete=models.SET_NULL)
	problem = models.ForeignKey(Problem, null=True, on_delete=models.SET_NULL)
	timestamp = models.DateTimeField(auto_now_add=True)
	correct = models.BooleanField(default=False)
	flags = models.CharField(max_length=200)
	answer = models.CharField(max_length=200)
	def __unicode__(self):
		return ("Problem " + str(self.problem_id) + " " + self.student.andrew)

class ActivitySubmission(models.Model):
	studentgroup = models.ForeignKey(StudentGroup, null=True, on_delete=models.SET_NULL)
	activity = models.ForeignKey(Activity, null=True, on_delete=models.SET_NULL)
	timestamp = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return ("Activity " + str(self.problem) + " " + Student.objects.get(pk=self.student).andrew)


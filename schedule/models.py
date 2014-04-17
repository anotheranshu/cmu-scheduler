from django.db import models
from django.contrib.auth.models import User

# Some helper functions.  Yeah, this is probably bad style.
def problem_field_to_list(myfield):
  return map(lambda x: int(x), myfield.split())

# Create your models here.

class Course(models.Model):
  course_num = models.IntegerField(default=0)
  tree_type = models.CharField(max_length=10)
  is_starter = models.BooleanField(default=False)
  prereq_indices = models.CommaSeparatedIntegerField(max_length=150)
  postreq_indices = models.CommaSeparatedIntegerField(max_length=150)
  description = models.CharField(max_length=9001)
  node_id = models.IntegerField(primary_key=True)
  title = models.CharField(max_length=200)
  def __unicode__(self):
    return (self.course_id + ": " + self.title)

class Student(models.Model):
  user = models.OneToOneField(User)
  andrew = models.CharField(max_length=100)
  taken_courses = models.CommaSeparatedIntegerField(max_length=3000)
  is_cs = models.BooleanField(default=True)
  sems_left = models.IntegerField(default=8)

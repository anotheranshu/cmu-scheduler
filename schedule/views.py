# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from schedule.models import *
from django.utils import simplejson
from schedule.helpers import *
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib import messages

def index(request, optargs={}):
  user = None


  if (request.user.is_authenticated()):
    user = request.user
  else:
    return HttpResponseRedirect(reverse('login'))


  if (user.student.is_instructor):
    activity_list = Activity.objects.all()
    return render(request, 'puzzle/instructor_hub.html', {'activities': activity_list})
  else:
    problem_list = map(lambda x: Problem.objects.get(pk=x), current_problems(user.student))
    activity_list = map(lambda x: Activity.objects.get(pk=x), current_activities(user.student))
    completed_problems = map(lambda x: Problem.objects.get(pk=x), problem_field_to_list(user.student.group.solved_problems))
    completed_activities = map(lambda x: Activity.objects.get(pk=x), problem_field_to_list(user.student.group.solved_activities))
    return render(request, 'puzzle/student_hub.html', {'current_problems': problem_list, 'current_activities': activity_list, 'completed_problems': completed_problems, 'completed_activities': completed_activities})

def login(request):
  return render(request, 'puzzle/login.html', {})

def logout_view(request):
  logout(request)
  return HttpResponseRedirect(reverse('login'))

def submit(request):
  if (request.user.is_authenticated()):
    problem_num = 0
    answer = ""
    student = request.user.student
    try:
      problem_num = int(request.POST['problem'])
      answer = request.POST['answer']
    except(KeyError):
      return HttpResponse(simplejson.dumps({'error': 'Invalid Request'}), content_type="application/json")
    else:
      if has_problem_access(student, problem_num):
        response = {'problem': problem_num}
        submission_code = process_submission(student, answer, problem_num)
        if (submission_code == 1):
          activity = Problem.objects.get(pk=problem_num).activity
          if (activity):
            return HttpResponseRedirect(reverse('activity', args=(activity.id,)))
          else:
            return HttpResponseRedirect(reverse('index'))
        elif (submission_code == 0):
          messages.error(request, "Sorry, that's incorrect.")
          return HttpResponseRedirect(reverse('problem', args=(problem_num,)))
        else:
          messages.error(request, "You've exceeded the maximum daily submissions for that problem.  Try again tomorrow!")
          return HttpResponseRedirect(reverse('index'))
        return HttpResponse(simplejson.dumps(response), content_type="application/json")
      else:
        #TODO, notify instructors that this has occured, as it shouldn't except in cheating cases
        return HttpResponse("You don't have access to this problem yet.")
  else:
    return HttpResponseForbidden()

def checkin(request):
  if (request.user.is_authenticated() and request.user.student.is_instructor):
    activity_num = 0
    student_andrew = ""
    try:
      activity_num = int(request.POST['activity'])
      student_andrew = request.POST['andrew']
    except(KeyError):
      return HttpResponse(simplejson.dumps({'error': 'Invalid Request'}), content_type="application/json")
    else:
      process_checkin(student_andrew, activity_num)
      return HttpResponseRedirect(reverse('index'))
  else:
    return HttpResponseForbidden()

def display_problem(request, pnum):
  problem_num = int(pnum)
  if (request.user.is_authenticated() and has_problem_access(request.user.student, problem_num)):
    arr = map(lambda x: "graphs/game" + str(x) + ".png", range(1, 9))
    return render(request, 'puzzle/problems/' + Problem.objects.get(pk=problem_num).file_name + '.html', {"problem": problem_num, "arr": arr})
  else:
    return HttpResponseForbidden()

def serve_static(request, template):
  return render(request, 'parchment.txt')

def serve_static_tome(request):
  return render(request, 'tome.txt')

def display_activity(request, pnum):
  activity_num = int(pnum)
  if (request.user.is_authenticated() and has_activity_access(request.user.student, activity_num)):
    return render(request, 'puzzle/activities/' + Activity.objects.get(pk=activity_num).file_name + '.html', {"activity": activity_num})
  else:
    return HttpResponseForbidden()

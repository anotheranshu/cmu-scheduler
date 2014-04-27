# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from schedule.models import *
from django.utils import simplejson
from schedule.helpers import *
from django.contrib.auth import logout, authenticate, login
from django.core.urlresolvers import reverse
from django.contrib import messages
import scripts.audit as audit
import scripts.authenticate as cmu_auth
from scripts.schedule_to_json import getJson


def index(request, optargs={}):
  user = None
  if (request.user.is_authenticated()):
    user = request.user
  else:
    return HttpResponseRedirect(reverse('login'))
  return render(request,'puzzle/student_hub.html')

def login_view(request):
  return render(request, 'puzzle/login.html', {})

def logout_view(request):
  logout(request)
  return HttpResponseRedirect(reverse('login'))

def about(request):
  return render(request, 'puzzle/about.html', {})

def display_activity(request, pnum):
  activity_num = int(pnum)
  if (request.user.is_authenticated() and has_activity_access(request.user.student, activity_num)):
    return render(request, 'puzzle/activities/' + Activity.objects.get(pk=activity_num).file_name + '.html', {"activity": activity_num})
  else:
    return HttpResponseForbidden()

def auth_user(request):
  myandrew = request.POST["username"]
  mypassword = request.POST["password"]
  wantedstr = request.POST["wanted"]
  want = []
  if wantedstr is not "":
    want = map (lambda x: int(x), ("".join(wantedstr.split())).split(","))
  if cmu_auth.myauth(myandrew, mypassword) is not None:
    user = authenticate(username=myandrew, password=myandrew)
    if user is None:
      make_student(myandrew, mypassword)
      user = authenticate(username=myandrew, password=myandrew)
    login(request, user)
    return render(request, 'puzzle/student_hub.html', {"myjson": getJson(myandrew, mypassword, 0, want)})
  return render(request, 'puzzle/login.html')
  
      

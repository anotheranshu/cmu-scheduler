from django.conf.urls import patterns, include, url

from schedule import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'puzzle/login.html'}, name='login'),
	url(r'^about/$', views.about, name='about'),
	url(r'^profile/', views.index, name='profile'),
	url(r'^submit/$', views.submit, name='submit'),
	url(r'^checkin/$', views.checkin, name='checkin'),
	url(r'^problems/(?P<pnum>\d+)/$', views.display_problem, name='problem'),
	url(r'^activities/(?P<pnum>\d+)/$', views.display_activity, name='activity'),
)

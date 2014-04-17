from django.conf.urls import patterns, include, url

from schedule import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^login/$', views.login_view, name='login'),
	url(r'^about/$', views.about, name='about'),
	url(r'^profile/', views.index, name='profile'),
  url(r'^login_transmit/$', views.auth_user, name='auth_user')
)

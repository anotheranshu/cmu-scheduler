from django.conf.urls import patterns, include, url

from schedule import views
#Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', include('schedule.urls')),
	url(r'^puzzle/', include('schedule.urls')),
	url(r'^accounts/', include('schedule.urls'))


    # Examples:
    # url(r'^$', 'puzzlehunt.views.home', name='home'),
    # url(r'^puzzlehunt/', include('puzzlehunt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

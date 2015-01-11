from django.conf.urls import patterns, url
from django.conf import settings

from main.views import *

urlpatterns = patterns('',
	url(r'^$', CaptureListView.as_view(), name='home'),
	url(r'^capture/create/$', CaptureCreate.as_view(), name='capture-create'),
	url(r'^capture/(?P<pk>\d+)/$', CaptureUpdate.as_view(), name='capture-update'),
	url(r'^echo/', echo, name='echo'),
)


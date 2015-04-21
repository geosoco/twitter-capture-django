from django.conf.urls import patterns, url, include
from django.conf import settings

from main.views import *

urlpatterns = patterns('',
	url(r'^$', CaptureListView.as_view(), name='home'),
	url(r'^archive/$', ArchiveListView.as_view(), name='archived-list'),
	url(r'^capture/create/$', CaptureCreate.as_view(), name='capture-create'),
	url(r'^capture/update/(?P<pk>\d+)/$', CaptureUpdate.as_view(), name='capture-update'),
	url(r'^capture/(?P<pk>\d+)/$', CaptureDetails.as_view(), name='capture-details'),
	url(r'^client/create/$', ClientCreate.as_view(), name='client-create'),
	url(r'^client/(?P<pk>\d+)/$', ClientDetail.as_view(), name='client-detail'),
	url(r'^client/$', ClientListView.as_view(), name='client-list'),
	url(r'^echo/', echo, name='echo'),
)


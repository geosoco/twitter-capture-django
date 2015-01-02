from django.conf.urls import patterns, url
from django.conf import settings

from main.views import *

urlpatterns = patterns('',
	url(r'^$', CaptureListView.as_view(), name='home'),
	url(r'^capture/create/$', CaptureCreate.as_view(), name='capture-create'),
	url(r'^capture/(?P<pk>\d+)/$', CaptureDetails.as_view(), name='capture-details'),
	#url(r'^clips/(?P<recording_id>\d+)/$', login_required(views.ClipListView.as_view()), name="cliplist"),
	#url(r'^transcription/create/$', login_required(views.TranscriptionCreate.as_view()), name="transcription_create"),

	#url(r'^test/$', views.test, name='test'),
)


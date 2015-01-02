from django.conf.urls import patterns, url
from django.conf import settings

from worker.views import *

urlpatterns = patterns('',
	url(r'^$', WorkerListView.as_view(), name='worker-list'),
	#url(r'^create/$', CaptureCreate.as_view(), name='capture-create'),
	#url(r'^(?P<pk>\d+)/$', CaptureDetails.as_view(), name='capture-details'),
	#url(r'^clips/(?P<recording_id>\d+)/$', login_required(views.ClipListView.as_view()), name="cliplist"),
	#url(r'^transcription/create/$', login_required(views.TranscriptionCreate.as_view()), name="transcription_create"),

	#url(r'^test/$', views.test, name='test'),
)


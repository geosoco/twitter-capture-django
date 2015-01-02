from django.conf.urls import patterns, url
from django.conf import settings

from worker.views import *

urlpatterns = patterns('',
	url(r'^$', WorkerListView.as_view(), name='worker-list'),
	url(r'^create/$', WorkerCreate.as_view(), name='worker-create'),
	url(r'^(?P<pk>\d+)/$', WorkerDetails.as_view(), name='worker-details'),
)


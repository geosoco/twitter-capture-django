from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.shortcuts import render, render_to_response, get_object_or_404
from django import forms
import json

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.util import ErrorList
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict

from models import *

import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)


#
# Mixins
#

class AjaxableResponseMixin(object):
	"""
	Mixin to add AJAX support to a form.
	Must be used with an object-based FormView (e.g. CreateView)
	"""
	def form_invalid(self, form):
		response = super(AjaxableResponseMixin, self).form_invalid(form)
		return JsonResponse(form.errors, status=400)


	def form_valid(self, form):
		# We make sure to call the parent's form_valid() method because
		# it might do some processing (in the case of CreateView, it will
		# call form.save() for example).
		logger.info("form is valid")

		#data = serializers.serialize('json', form)
		logger.info("form data: %s"%(str(form.fields['text'])))
		response = super(AjaxableResponseMixin, self).form_valid(form)
		data = model_to_dict(self.object)
		return JsonResponse(data)




# Create your views here.

def test(request):
	return HttpResponse("test view")




class CaptureListView(ListView):
	"""
	Listview for Captures
	"""
	template_name = "capturejob/capture_list.html"
	context_object_by_name = "capture_list"
	paginate_by = 10
	model = CaptureJob



	#def get_queryset(self):
		#job_id = self.kwargs['job_id']
		#self.job = get_object_or_404(CaptureJob, pk=job_id)
		#return Clip.objects.filter(pk=self.job_id).order_by('offset').prefetch_related('transcription_set')

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(CaptureListView, self).get_context_data(**kwargs)
		# Add in a QuerySet of all the books
		#context['project'] = self.recording.project
		#context['recording'] = self.recording
		context['debug'] = serializers.serialize('json', self.get_queryset())
		#context['form'] = TranscriptionForm(initial={'user': self.request.user})
		#context['user_id'] = self.request.user.id
		#context['project_dir'] = settings.PROJECT_DIR
		#context['project_root'] = settings.PROJECT_ROOT
		#context['static_root'] = settings.STATIC_ROOT
		return context


class CaptureCreate(AjaxableResponseMixin, CreateView):
	model = CaptureJob
	fields = [ 'name', 'description', 'twitter_keywords' ]
	template = 'capturejob/create.html'



class CaptureDetails(AjaxableResponseMixin, DetailView):
	model = CaptureJob
	template = 'capturejob/detail.html'


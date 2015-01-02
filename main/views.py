from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound, JsonResponse
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django import forms

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict

from django.contrib.auth.decorators import login_required

from models import *

import logging
from datetime import datetime


# Get an instance of a logger
logger = logging.getLogger(__name__)


#
# Mixins
#

class LoginRequiredMixin(object):
    """A mixin that forces a login to view the CBTemplate."""
    
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)



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

		# data = serializers.serialize('json', form)
		#logger.info("form data: %s"%(str(form.fields['text'])))
		response = super(AjaxableResponseMixin, self).form_valid(form)
		data = model_to_dict(self.object)
		return JsonResponse(data)




# Create your views here.

def test(request):
	return HttpResponse("test view")




class CaptureListView(LoginRequiredMixin, ListView):
	"""
	Listview for Captures
	"""
	template_name = "capturejob/list.html"
	context_object_by_name = "capture_list"
	paginate_by = 10
	model = Job



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


class CaptureCreate(LoginRequiredMixin, CreateView):
	model = Job
	fields = [ 'name', 'description', 'twitter_keywords' ]
	template_name = 'capturejob/create.html'

	def form_valid(self, form):

		now = datetime.now()
		form.instance.created_by = self.request.user
		form.instance.status = Job.STATUS_CREATED

		return super(CaptureCreate, self).form_valid(form)



class CaptureDetails(LoginRequiredMixin, DetailView):
	model = Job
	template_name = 'capturejob/detail.html'



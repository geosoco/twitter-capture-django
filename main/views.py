from django.views.generic import View, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView

from django.core import serializers
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from rest_framework.authtoken.models import Token
import simplejson as json


from models import *

from base.views import LoginRequiredMixin

import logging
from datetime import datetime


# Get an instance of a logger
logger = logging.getLogger(__name__)



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

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(CaptureListView, self).get_context_data(**kwargs)
		context['debug'] = serializers.serialize('json', self.get_queryset())
		return context


class CaptureCreate(LoginRequiredMixin, CreateView):
	"""
	CreateView for Captures
	"""

	model = Job
	fields = [ 'name', 'description', 'twitter_keywords', 'assigned_worker' ]
	template_name = 'capturejob/create.html'

	def form_valid(self, form):

		now = datetime.now()
		form.instance.created_by = self.request.user
		form.instance.status = Job.STATUS_CREATED

		return super(CaptureCreate, self).form_valid(form)



class CaptureDetails(LoginRequiredMixin, DetailView):
	"""
	DetailView for Captures
	"""

	model = Job
	template_name = 'capturejob/detail.html'


class CaptureUpdate(LoginRequiredMixin, UpdateView):
	"""
	UpdateView for Captures
	"""

	model = Job
	fields = [ 'name', 'description', 'twitter_keywords' ]
	template_name = 'capturejob/create.html'

	def form_valid(self, form):
		now = datetime.now()
		form.instance.modified_by = self.request.user
		form.instance.modified_date = now

		old = Job.objects.get(pk=self.object.pk)

		logger.warn("doing modification")
		logger.warn("name: %s -> %s"%(old.name , form.instance.name))
		logger.warn("description: %s -> %s"%(old.description , form.instance.description))
		logger.warn("keywords: %s -> %s"%(self.object.twitter_keywords , form.instance.twitter_keywords))

		# create modification dictionary
		diff = {}
		if form.instance.name != old.name:
			diff['name'] = form.instance.name

		if form.instance.description != old.description:
			diff['description'] = form.instance.description

		if form.instance.twitter_keywords != old.twitter_keywords:
			diff['twitter_keywords'] = form.instance.twitter_keywords

		# serialize the text
		diff_text = json.dumps(diff)

		modification = JobModification(
				changes = diff_text,
				job = self.object,
				modified_by = self.request.user,
				modified_date = now
			)

		modification.save()

		return super(CaptureUpdate, self).form_valid(form)



class ClientCreate(LoginRequiredMixin, CreateView):
	"""
	Create view for making clients. Also creates 
	"""

	model = User
	fields = [ 'username', 'password']
	template_name = 'client/create.html'

	def get_success_url(self):
		return reverse('client-detail', args=(self.object.id,))

	def form_valid(self, form):
		response = super(ClientCreate, self).form_valid(form)

		# add the user to the capture_client group
		g = Group.objects.get(name='capture_client') 
		self.object.groups.add(g)

		# create auth token for the user
		Token.objects.get_or_create(user=self.object)
		return response


class ClientDetail(LoginRequiredMixin, DetailView):
	"""
	"""

	model = User
	fields = ['username', 'password']
	template_name = 'client/detail.html'


	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(ClientDetail, self).get_context_data(**kwargs)
		context['debug'] = serializers.serialize('json', self.get_queryset())

		return context	


class ClientListView(LoginRequiredMixin, ListView):
	"""
	"""

	template_name = "client/list.html"
	paginate_by = 10
	model = User


	def get_queryset(self):
		queryset = User.objects.filter(groups__name='capture_client')
		return queryset




# debug function to dump some header info
def echo(request):
	ls = []
	for k,v in request.META.iteritems():
		s = str(k) + ":" + str(v)
		ls.append(s)
		logger.error(s)

	return HttpResponse("<br/>".join(ls))


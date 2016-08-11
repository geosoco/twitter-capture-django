from django.views.generic import View, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView

from django.core import serializers
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import make_password
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


class MainAppView(LoginRequiredMixin, TemplateView):
	"""
	TemplateView
	"""
	template_name = "main/index.html"



class CaptureListView(LoginRequiredMixin, ListView):
	"""
	Listview for Captures
	"""

	template_name = "capturejob/list2.html"
	context_object_by_name = "capture_list"
	paginate_by = 10
	querset = queryset = Job.objects.exclude(deleted_date__isnull=False)

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(CaptureListView, self).get_context_data(**kwargs)
		context['debug'] = serializers.serialize('json', context['object_list'])
		#print repr([serializers.serialize('json', j) for j in context['job_list'] ])
		return context

class ArchiveListView(LoginRequiredMixin, ListView):
	"""
	Listview for Captures
	"""

	template_name = "capturejob/list.html"
	context_object_by_name = "capture_list"
	paginate_by = 10
	querset = queryset = Job.objects.exclude(archived_date__isnull=True)

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(ArchiveListView, self).get_context_data(**kwargs)

		return context


class CaptureCreate(LoginRequiredMixin, CreateView):
	"""
	CreateView for Captures
	"""

	model = Job
	fields = [ 'name', 'description', 'keywords', 'assigned_worker' ]
	template_name = 'capturejob/create.html'

	def get_form(self, form_class):
		form = super(CreateView, self).get_form(form_class)
		# make it required but only list ones that have items that have no created or running workers
		form.fields['assigned_worker'].required = True
		form.fields['assigned_worker'].queryset = User.objects.filter(groups__name='capture_client').exclude(job__archived_date__isnull=True)
		return form


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
	fields = [ 'name', 'description', 'keywords', 'assigned_worker' ]
	template_name = 'capturejob/create.html'

	def get_form(self, form_class):
		form = super(UpdateView, self).get_form(form_class)
		# disable setting this on update
		form.fields['assigned_worker'].widget.attrs['disabled'] = True
		return form

	def form_valid(self, form):
		now = datetime.now()
		form.instance.modified_by = self.request.user
		form.instance.modified_date = now

		old = Job.objects.get(pk=self.object.pk)

		logger.debug("doing modification")
		logger.debug(
			"name: %s -> %s", old.name, form.instance.name)
		logger.debug(
			"description: %s -> %s",
			old.description, form.instance.description)
		logger.debug(
			"keywords: %s -> %s",
			self.object.keywords, form.instance.keywords)

		# copy over the assigned worker
		form.instance.assigned_worker = old.assigned_worker

		# create modification dictionary
		diff = {}
		if form.instance.name != old.name:
			nd = {}
			nd['old'] = old.name
			nd['new'] = form.instance.name
			diff['name'] = nd

		if form.instance.description != old.description:
			desc = {}
			desc['old'] = old.description
			desc['new'] = form.instance.description
			diff['description'] = desc

		if form.instance.keywords != old.keywords:
			tk = {}
			tk['old'] = old.keywords
			tk['new'] = form.instance.keywords
			old_keywords = set([w.strip() for w in old.keywords.split(',')])
			new_keywords = set([w.strip() for w in form.instance.keywords.split(',')])
			additions = new_keywords - old_keywords
			deletions = old_keywords - new_keywords
			tk['additions'] = list(additions)
			tk['deletions'] = list(deletions)
			# set keywords dict
			diff['keywords'] = tk

		# serialize the text
		diff_text = json.dumps(diff)

		modification = JobModification(
			changes=diff_text,
			job=self.object,
			modified_by=self.request.user,
			modified_date=now
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
		form.instance.password = make_password(form.instance.password)

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


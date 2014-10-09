from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, render_to_response, get_object_or_404
from django import forms
import json

from django.views.generic import View, ListView
from django.views.generic.edit import CreateView

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.util import ErrorList
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict

import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)



# Create your views here.

def test(request):
	return HttpResponse("test view")
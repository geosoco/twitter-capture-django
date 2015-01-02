import os
import logging
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Get an instance of a logger
logger = logging.getLogger(__name__)



class CaptureJob(models.Model):
	"""
		Model for a capture
	"""
	STATUS_CREATED = 0
	STATUS_STARTED = 1
	STATUS_STOPPED = 2

	STATUS_CHOICES = (
		(STATUS_CREATED, 'created'),
		(STATUS_STARTED, 'started'),
		(STATUS_STOPPED, 'stopped'),
	)


	name = models.CharField(max_length=256)
	description = models.TextField()

	creation_date = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, null=True, blank=True)

	twitter_keywords = models.TextField()

	status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_CREATED)

	task_id = models.IntegerField(null=True, blank=True)

	first_started = models.DateTimeField(null=True, blank=True)
	started = models.DateTimeField(null=True, blank=True)
	stopped = models.DateTimeField(null=True, blank=True)




class CaptureJobModification(models.Model):
	"""
		Model for change history of a capturejob 
	"""
	changes = models.TextField()

	job = models.ForeignKey(CaptureJob, blank=True)

	modification_date = models.DateTimeField(auto_now_add=True)
	modified_by = models.ForeignKey(User, null=True, blank=True)



class CaptureUpdate(models.Model):
	"""
		Model for capture update / update 
	"""

	date = models.DateTimeField(auto_now_add=True)

	count = models.IntegerField()
	total_count = models.IntegerField()





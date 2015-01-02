import os
import logging
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.urlresolvers import reverse

from base.models import FullAuditModel, ModifiedByMixin
from worker.models import Worker


# Get an instance of a logger
logger = logging.getLogger(__name__)



	


class Job(FullAuditModel):
	"""
		Model for a capture
	"""
	STATUS_UNKNOWN = 0
	STATUS_CREATED = 1
	STATUS_STARTING = 2
	STATUS_STARTED = 3
	STATUS_STOPPING = 4
	STATUS_STOPPED = 5
	STATUS_UNRESPONSIVE = 6
	STATUS_DEAD = 7

	STATUS_CHOICES = (
		(STATUS_UNKNOWN, 'unknown'),
		(STATUS_CREATED, 'created'),
		(STATUS_STARTING, 'starting'),
		(STATUS_STARTED, 'started'),
		(STATUS_STOPPING, 'stopping'),
		(STATUS_STOPPED, 'stopped'),
		(STATUS_UNRESPONSIVE, 'unresponsive'),
		(STATUS_DEAD, 'dead'),
	)


	name = models.CharField(max_length=256)
	description = models.TextField()

	twitter_keywords = models.TextField()

	status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_CREATED)

	task_id = models.IntegerField(null=True, blank=True)

	first_started = models.DateTimeField(null=True, blank=True)
	started = models.DateTimeField(null=True, blank=True)
	stopped = models.DateTimeField(null=True, blank=True)

	assigned_worker = models.ForeignKey(Worker, blank=True)

	def get_absolute_url(self):
		return reverse('capture-details', kwargs={ 'pk': self.pk, })



class JobModification(ModifiedByMixin):
	"""
		Model for change history of a capturejob 
	"""
	changes = models.TextField()

	job = models.ForeignKey(Job, blank=True)



class Update(models.Model):
	"""
		Model for capture update / update 
	"""

	date = models.DateTimeField(auto_now_add=True)

	count = models.IntegerField()
	total_count = models.IntegerField()






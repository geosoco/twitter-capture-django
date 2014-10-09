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
	name = models.CharField(max_length=256)
	description = models.TextField()

	creation_date = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, null=True, blank=True)

	twitter_keywords = models.TextField()

	task_id = models.IntegerField(null=True, blank=True)


class CaptureJobModification(models.Model):
	"""
		Model for change history of a capturejob 
	"""
	changes = models.TextField()

	job = models.ForeignKey(CaptureJob, blank=True)

	modification_date = models.DateTimeField(auto_now_add=True)
	modified_by = models.ForeignKey(User, null=True, blank=True)


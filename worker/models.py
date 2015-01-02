from django.db import models
from base.models import FullAuditModel


class Worker(FullAuditModel):
	"""
		Model for capture workers (the machines doing the capturing)
	"""

	name = models.CharField(max_length=256)
	description = models.TextField()

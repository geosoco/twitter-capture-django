from django.db import models
from base.models import FullAuditModel
from django.contrib.auth.models import User
from datetime import datetime


class Worker(FullAuditModel):
	"""
		Model for capture workers (the machines doing the capturing)
	"""

	description = models.TextField()
	last_update = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, unique=True)


	def has_connected(self):
		return last_update is not None


	def connection_status(self):
		if self.last_update is None:
			return "never connected"

		# calculate duration since last update
		now = datetime.now()
		dur = now - self.last_update

		secs = dur.total_seconds()
		if secs < 30:
			return "connected"
		elif secs < 60:
			return "late"
		else:
			return "disconnected"




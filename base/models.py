from django.db import models
from django.contrib.auth.models import User


class CreatedByMixin(models.Model):
	created_date = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, null=True, blank=True)

	class Meta:
		abstract = True

class ModifiedByMixin(models.Model):
	modified_date = models.DateTimeField(auto_now=True)
	modified_by = models.ForeignKey(User, null=True, blank=True)

	class Meta:
		abstract = True	


class DeletedByMixin(models.Model):
	deleted_date = models.DateTimeField(auto_now=True, null=True, blank=True)
	deleted_by = models.ForeignKey(User, null=True, blank=True)

	class Meta:
		abstract = True

class FullAuditModel(CreatedByMixin, ModifiedByMixin, DeletedByMixin):

	class Meta:
		abstract = True
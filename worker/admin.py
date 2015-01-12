from django.contrib import admin
from base.admin import CreatedByBaseAdmin, FullAuditBaseAdmin
from worker.models import Worker


class WorkerAdmin(FullAuditBaseAdmin):
	"""
	Worker Admin
	"""

	list_display = ('id', 'user_username', 'user_firstname', 'last_update', 'created_by', 'created_date', 'modified_by', 'modified_date', 'deleted_by', 'deleted_date')

	def user_username(self):
		return self.user.username

	def user_firstname(self):
		return self.user.firstname

#
# register admin handlers
#

admin.site.register(Worker,WorkerAdmin)


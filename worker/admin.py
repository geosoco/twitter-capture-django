from django.contrib import admin
from base.admin import CreatedByBaseAdmin, FullAuditBaseAdmin
from worker.models import Worker


class WorkerAdmin(FullAuditBaseAdmin):
	"""
	Worker Admin
	"""

	list_display = ('name', 'description', 'created_by', 'created_date', 'modified_by', 'modified_date', 'deleted_by', 'deleted_date')


#
# register admin handlers
#

admin.site.register(Worker,WorkerAdmin)


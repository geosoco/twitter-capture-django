from django.contrib import admin
from workers import models


class WorkerAdmin(CreatedByBaseAdmin):
	"""
	Worker Admin
	"""

	list_display = ('name', 'description', 'created_by', 'created_date', 'twitter_keywords')


#
# register admin handlers
#

admin.site.register(Worker,WorkerAdmin)


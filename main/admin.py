from django.contrib import admin
from main.models import *
from base.admin import CreatedByBaseAdmin, FullAuditBaseAdmin

# Register your models here.





#
#
#
class JobAdmin(FullAuditBaseAdmin):
	"""
	Job Admin
	"""

	list_display = ('name', 'description', 'twitter_keywords')



#
#
#
class JobModificationAdmin(CreatedByBaseAdmin):
	"""
	JobModification Admin
	"""

	list_display = ('job_name', 'job_description', 'modified_by', 'modified_date' )
	readonly_fields = ('job_name', 'job_description')


	def job_name(self,obj):
		return obj.job.name

	def job_description(self,obj):
		return obj.job.description



class UpdateAdmin(admin.ModelAdmin):
	"""
	Update Admin model
	"""

	list_display = ('id', 'date', 'count', 'total_count', 'rate')
	readonly_fields = ('id', 'date', 'count', 'total_count', 'rate')


#
# register admin handlers
#

admin.site.register(Job,JobAdmin)
admin.site.register(JobModification,JobModificationAdmin)



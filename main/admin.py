from django.contrib import admin
from main.models import *

# Register your models here.


#
#
#
class CreatedByBaseAdmin(admin.ModelAdmin):
	""" Base class for handling created by stuff """

	readonly_fields = ('created_by', 'creation_date')

	def save_formset(self, request, form, formset, change):
		instances = formset.save(commit=False)
		for instance in instances:
			if not change:
				instance.created_by = request.user
				instance.save()
		formset.save()

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_by = request.user
		obj.save()



#
#
#
class CaptureJobAdmin(CreatedByBaseAdmin):
	"""
	CaptureJob Admin
	"""

	list_display = ('name', 'description', 'created_by', 'creation_date', 'twitter_keywords')



#
#
#
class CaptureJobModificationAdmin(CreatedByBaseAdmin):
	"""
	CaptureJobModification Admin
	"""

	list_display = ('job_name', 'job_description', 'modified_by', 'modification_date' )
	readonly_fields = ('job_name', 'job_description')


	def job_name(self,obj):
		return obj.job.name

	def job_description(self,obj):
		return obj.job.description


#
# register admin handlers
#

admin.site.register(CaptureJob,CaptureJobAdmin)
admin.site.register(CaptureJobModification,CaptureJobModificationAdmin)



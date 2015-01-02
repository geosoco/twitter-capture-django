from worker.models import Worker
from django.views.generic import View, ListView

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder



#class WorkerListView(LoginRequiredMixin, ListView):
class WorkerListView(ListView):
	"""
	Listview for Workers
	"""
	template_name = "list.html"
	context_object_by_name = "worker_list"
	paginate_by = 10
	model = Worker



	#def get_queryset(self):
		#job_id = self.kwargs['job_id']
		#self.job = get_object_or_404(CaptureJob, pk=job_id)
		#return Clip.objects.filter(pk=self.job_id).order_by('offset').prefetch_related('transcription_set')

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(WorkerListView, self).get_context_data(**kwargs)
		# Add in a QuerySet of all the books
		#context['project'] = self.recording.project
		#context['recording'] = self.recording
		context['debug'] = serializers.serialize('json', self.get_queryset())
		#context['form'] = TranscriptionForm(initial={'user': self.request.user})
		#context['user_id'] = self.request.user.id
		#context['project_dir'] = settings.PROJECT_DIR
		#context['project_root'] = settings.PROJECT_ROOT
		#context['static_root'] = settings.STATIC_ROOT
		return context
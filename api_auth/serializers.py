from django.contrib.auth.models import User, Group
from main.models import Job, JobModification, Update
from worker.models import Worker
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class UpdateSimpleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Update
		fields = ('date', 'total_count', 'rate')

class JobSerializer(serializers.ModelSerializer):
	status = serializers.ChoiceField(choices=Job.STATUS_CHOICES)
	#updates = serializers.SerializerMethodField()

	#def get_updates(self, job):
	#	updates_queryset = 	Update.objects.order_by('-date')[:20]
	#	serializer = UpdateSimpleSerializer(instance=updates_queryset, many=True, context=self.context)
	#	return serializer.data

	class Meta:
		model = Job
		fields = ('id', 'url', 'name', 'description', 'twitter_keywords', 'status', 'task_id', 'first_started', 'started', 'stopped', 'assigned_worker', 'total_count', 'rate', 'ping_date', 'created_by', 'created_date', 'modified_by', 'modified_date', 'deleted_by', 'deleted_date')
		partial = True
		#read_only_fields = ('updates',)

class JobIdSerializer(serializers.ModelSerializer):
	class Meta:
		model = Job
		fields = ('id')


class UpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Update
		fields = ('date', 'count', 'total_count', 'rate', 'job')
		

class ClientSerializer(serializers.ModelSerializer):
	active_jobs = serializers.SerializerMethodField()


	def get_active_jobs(self, obj):
		active_jobs = Job.objects.filter(assigned_worker=obj, archived_date__isnull=True)
		serializer = JobSerializer(active_jobs, context=self.context, many=True)
		return serializer.data

	class Meta:
		model = User
		fields = ('id', 'username', 'last_login', 'active_jobs')
		depth = 2


class WorkerSerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)


	class Meta:
		model = Worker
		fields = ('url', 'user', 'description', 'last_update')



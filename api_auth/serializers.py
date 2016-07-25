from django.contrib.auth.models import User, Group
from main.models import Job, JobModification, Update
from worker.models import Worker
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class UserReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)
        read_only_fields = ('username',)


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
	#assigned_worker_details = UserReadOnlySerializer()
	assigned_worker_username = serializers.CharField(read_only=True, source="assigned_worker.username")
	created_by_username = serializers.CharField(read_only=True, source="created_by.username")
	modified_by_username = serializers.CharField(read_only=True, source="modified_by.username")
	recent_update = serializers.SerializerMethodField()

	#updates = serializers.SerializerMethodField()

	#def get_updates(self, job):
	#	updates_queryset = 	Update.objects.order_by('-date')[:20]
	#	serializer = UpdateSimpleSerializer(instance=updates_queryset, many=True, context=self.context)
	#	return serializer.data

	def validate_assigned_worker(self, value):

		# ignore if it isn't changing
		if self.instance is None or value == self.instance.assigned_worker:
			return value

		# validate against none
		if value is None:
			raise serializers.ValidationError("This job must be assigned to a valid client.")

		# check that the client isn't already assigned
		active_jobs = Job.objects.filter(assigned_worker=value, archived_date__isnull=True)
		if self.instance is not None and self.instance.id is not None:
			active_jobs = active_jobs.exclude(pk=self.instance.id)
		count_active_jobs = active_jobs.count()
		
		if count_active_jobs > 0:
			raise serializers.ValidationError("Client is already assigned, choose another job")

		# return validation value
		return value

	def get_recent_update(self, job):
		updates = Update.objects.filter(job=job).order_by('-date')[:1]
		if updates is not None and updates.count() > 0:
			serializer = UpdateSimpleSerializer(
				instance=updates[0],
				many=False)
			return serializer.data
		else:
			return {}

	class Meta:
		model = Job
		fields = (
			'id', 'url', 'name', 'description', 'twitter_keywords',
			'status', 'task_id', 'first_started', 'started', 'stopped',
			'assigned_worker', 'assigned_worker_username', 'total_count',
			'rate', 'ping_date', 'archived_date', 'archived_by',
			'created_by', 'created_by_username', 'created_date',
			'modified_by', 'modified_by_username', 'modified_date',
			'deleted_by', 'deleted_date', 'recent_update')
		read_only_fields = (
			'assigned_worker_username',
			'archived_by',
			'recent_update')
		partial = True



class JobIdSerializer(serializers.ModelSerializer):
	class Meta:
		model = Job
		fields = ('id',)


class UpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Update
		fields = ('date', 'count', 'total_count', 'rate', 'job')


class TokenSerializer(serializers.ModelSerializer):
	class Meta:
		model = Token
		fields = ('key', 'created')

class ClientSerializer(serializers.ModelSerializer):
	active_jobs = serializers.SerializerMethodField()
	auth_token = TokenSerializer(read_only=True)


	def get_active_jobs(self, obj):
		active_jobs = Job.objects.filter(assigned_worker=obj, archived_date__isnull=True)
		serializer = JobSerializer(active_jobs, context=self.context, many=True)
		return serializer.data

	class Meta:
		model = User
		fields = (
			'id', 'username', 'last_login', 'active_jobs', 'auth_token',)
		depth = 2


class WorkerSerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)


	class Meta:
		model = Worker
		fields = ('url', 'user', 'description', 'last_update')


class JobModificationSerializer(serializers.ModelSerializer):
	modified_by_username = serializers.CharField(
		read_only=True,
		source="modified_by.username")
	changes = serializers.JSONField()

	class Meta:
		model = JobModification
		fields = ('id', 'changes', 'job', 'modified_by', 'modified_by_username',)


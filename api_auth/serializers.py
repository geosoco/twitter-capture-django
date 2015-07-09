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


class UpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Update
		fields = ('date', 'count', 'total_count', 'rate', 'job')
		

class WorkerSerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)


	class Meta:
		model = Worker
		fields = ('url', 'user', 'description')



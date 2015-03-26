from django.contrib.auth.models import User, Group
from main.models import Job, JobModification, Update
from worker.models import Worker
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class JobSerializer(serializers.ModelSerializer):
	status = serializers.ChoiceField(choices=Job.STATUS_CHOICES)

	class Meta:
		model = Job
		fields = ('url', 'name', 'description', 'twitter_keywords', 'status', 'task_id', 'first_started', 'started', 'stopped', 'assigned_worker')


class UpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Update
		fields = ('date', 'count', 'total_count', 'rate', 'job')
		

class WorkerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Worker
		fields = ('url', 'name', 'description')



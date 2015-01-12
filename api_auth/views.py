from django.contrib.auth.models import User, Group
from main.models import Job, JobModification, Update
from worker.models import Worker
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api_auth.serializers import *



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class JobViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows Jobs to be viewed or edited.
	"""
	queryset = Job.objects.all()
	serializer_class = JobSerializer
	authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
	permission_classes = (IsAuthenticated,)

class UpdateViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows Job Updates to be viewed or edited.
	"""
	queryset = Update.objects.all()
	serializer_class = UpdateSerializer
	authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
	permission_classes = (IsAuthenticated,)

class WorkerViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows Worker to be viewed or edited.
	"""
	queryset = Worker.objects.all()
	serializer_class = WorkerSerializer	
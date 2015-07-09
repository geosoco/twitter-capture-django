from django.contrib.auth.models import User, Group
from main.models import Job, JobModification, Update
from worker.models import Worker
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api_auth.serializers import *
from rest_framework import filters
import django_filters
from datetime import datetime



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('pk') == 'current' and request.user:
            kwargs['pk'] = request.user.pk

        return super(UserViewSet, self).dispatch(request, *args, **kwargs)



class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


class JobFilterSet(django_filters.FilterSet):
    active = django_filters.BooleanFilter(name="deleted_date__isnull")
    class Meta:
        model = Job
        fields = ['active']

class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Jobs to be viewed or edited.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    filter_class = JobFilterSet

    def perform_create(self, serializer):
        serializer.created_by = self.request.user
        serializer.created_date = datetime.now()
        serializer.save()

    def perform_destroy(self, serializer):
        serializer.deleted_by = self.request.user
        serializer.deleted_date = datetime.now()
        serializer.save()

class ActiveJobViewSet(viewsets.ModelViewSet):
    """
    API endpoint for active jobs of the current user
    """
    serializer_class = JobSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = Job.objects.filter(assigned_worker=self.request.user).exclude(deleted_date__isnull=False)
        return qs



class UpdateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Job Updates to be viewed or edited.
    """
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


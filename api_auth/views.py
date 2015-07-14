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
    active = django_filters.BooleanFilter(name="archived_date__isnull")
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


    def has_value_changed(self, instance, data, name):
        if name in data:
            if data[name] != getattr(instance, name):
                return True
        elif getattr(instance, name):
            return True
        return False

    def perform_update(self, serializer):
        kwargs = {}
        serializer.modified_by = self.request.user
        serializer.modified_date = datetime.now()

        # grab objects to compare
        instance = self.get_object()
        data = serializer.validated_data

        if self.has_value_changed(instance, data, 'archived_date'):
            if 'archived_date' in  data and data['archived_date'] is not None:
                serializer.validated_data['archived_by'] = self.request.user

        
        # set ping date if right item
        if instance.assigned_worker is not None and self.request.user.id == instance.assigned_worker.id:
            data['ping_date'] = datetime.now()
            kwargs['ping_date'] = datetime.now()

        serializer.save()



class ActiveJobViewSet(viewsets.ModelViewSet):
    """
    API endpoint for active jobs of the current user
    """
    serializer_class = JobSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = Job.objects.filter(assigned_worker=self.request.user).exclude(archived_date__isnull=False)
        return qs



class UpdateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Job Updates to be viewed or edited.
    """
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint for the Users that are clients
    """
    queryset = User.objects.filter(groups__name='capture_client')
    serializer_class = ClientSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


class WorkerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing workers
    """
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


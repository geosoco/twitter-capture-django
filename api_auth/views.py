from django.contrib.auth.models import User, Group
from main.models import Job, JobModification, Update
from worker.models import Worker
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api_auth.serializers import *
from rest_framework import filters
import django_filters
from datetime import datetime
from django.db import connection
import simplejson as json




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



#class UpdateViewSet(viewsets.ModelViewSet):
#    """
#    API endpoint that allows Job Updates to be viewed or edited.
#    """
#    queryset = Update.objects.all()
#    serializer_class = UpdateSerializer
#    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
#    permission_classes = (IsAuthenticated,)


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


class UpdateViewSet2(viewsets.ViewSet):
    """
    """

    def serialize(self, cursor, delta):
        result = {}
        for row in cursor:
            job_id = row[0]
            date = row[1]
            unixdate = row[2]
            cnt = row[3]

            if job_id not in result:
                job = {
                    "job_id": job_id,
                    "date": date.isoformat(),
                    "unixdate": unixdate,
                    "counts": [],
                    "delta_secs": delta
                }
                result[job_id] = job

            result[job_id]["counts"].append(int(cnt))

        return Response(result)


    def run_query(self, request, query, params = None):
        cursor = connection.cursor()
        cursor.execute(query, params)

        result = self.serialize(cursor, 60)

        cursor.close()

        return result


    def list(self,request):
        query = """
        select j.id as job_id, from_unixtime(FLOOR(unix_timestamp(date)/60)*60) as date, FLOOR(unix_timestamp(date)/60)*60 as unixdate, sum(count) as cnt, round(avg(count),1) as average
        from capture.main_update
        inner join capture.main_job j on j.id = job_id
        where ISNULL(j.archived_date) and date > DATE_SUB(utc_timestamp(), INTERVAL 1 HOUR)
        group by j.id, unixdate; 
        """
        return self.run_query(request, query)

    def retrieve(self, request, pk=None):
        query = """
        select job_id, from_unixtime(FLOOR(unix_timestamp(date)/60)*60) as date, FLOOR(unix_timestamp(date)/60)*60 as unixdate, sum(count) as cnt, round(avg(count),1) as average
        from capture.main_update
        where job_id = %s and date > DATE_SUB(utc_timestamp(), INTERVAL 1 HOUR)
        group by unixdate;
        """
        return self.run_query(request, query, [pk])


#    def retrieve(self, request, pk=None):
#        pass



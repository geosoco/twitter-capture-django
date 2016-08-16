from django.contrib.auth.models import User, Group
from main.models import Job, Update, JobModification
from worker.models import Worker
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import (
    SessionAuthentication, BasicAuthentication, TokenAuthentication)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from api_auth.serializers import (
    UserSerializer, GroupSerializer, JobSerializer, ClientSerializer,
    UpdateSerializer, WorkerSerializer, JobModificationSerializer)
import django_filters
from django.db import connection, transaction
from django.utils import timezone
import json
from rest_framework_filters import backends
import rest_framework_filters as filters


class TestFilter(backends.DjangoFilterBackend):
    def __init__(self):
        print ">> creating"
        print super(TestFilter, self).__init__
        for base in self.__class__.__bases__:
            print base.__module__, base.__name__
        return super(TestFilter, self).__init__()

    def get_filter_class(self, view, queryset=None):
        print ">> get_filter_class"
        if queryset:
            print queryset.query
        else:
            print "no queryset"
        ret = super(TestFilter, self).get_filter_class(view, queryset)

        if queryset:
            print queryset.query
        else:
            print "no queryset"

        print "\n>> got back", ret
        od = ret().get_filters()
        print "\n>> -"
        print json.dumps(od)
        #print "\n>> +", ret(view.request.query_params, queryset=queryset).qs

        return ret

    def filter_queryset(self, request, queryset, view):
        print ">> filter_queryset"
        return super(TestFilter, self).filter_queryset(
            request, queryset, view)

    def get_filters(self):

        print ">> get_filters"
        ret = super(TestFilter, self).get_filter()

        print json.dumps(ret)
        print "\n"

        return ret


def has_value_changed(instance, data, name):
    if name in data:
        if data[name] != getattr(instance, name):
            return True
    elif getattr(instance, name):
        return True
    return False


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, TokenAuthentication)
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
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


class JobFilterSet(filters.FilterSet):
    active = filters.BooleanFilter(name="archived_date", lookup_expr="isnull")

    class Meta:
        model = Job
        fields = ['active']


class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Jobs to be viewed or edited.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    filter_class = JobFilterSet
    #filter_backends = (backends.DjangoFilterBackend,)
    #filter_backends = (TestFilter,)

    def perform_create(self, serializer):
        serializer.created_by = self.request.user
        serializer.created_date = timezone.now()
        serializer.save()

    def perform_destroy(self, serializer):
        serializer.deleted_by = self.request.user
        serializer.deleted_date = timezone.now()
        serializer.save()

    @transaction.atomic
    def perform_update(self, serializer):
        kwargs = {}
        now = timezone.now()
        serializer.modified_by = self.request.user
        serializer.modified_date = now

        # grab objects to compare
        instance = self.get_object()
        data = serializer.validated_data

        if has_value_changed(instance, data, 'archived_date'):
            if data.get('archived_date', None) is not None:
                serializer.validated_data['archived_by'] = self.request.user

        # set ping date if right item
        if (instance.assigned_worker is not None and
                self.request.user.id == instance.assigned_worker.id):
            data['ping_date'] = timezone.now()
            kwargs['ping_date'] = timezone.now()

        # build other diff
        diff = {}
        if has_value_changed(instance, data, "name"):
            nd = {}
            nd['old'] = data.get('name', None)
            nd['new'] = instance.name
            diff['name'] = nd

        if has_value_changed(instance, data, "description"):
            desc = {}
            desc['old'] = data.get('description', None)
            desc['new'] = instance.description
            diff['description'] = desc

        if has_value_changed(instance, data, "keywords"):
            tk = {}
            old_kws = data.get('keywords', {})
            new_kws = instance.keywords
            tk['old'] = old_kws
            tk['new'] = new_kws
            old_keywords = set([w.strip() for w in old_kws.split(',')])
            new_keywords = set([w.strip() for w in new_kws.split(',')])
            additions =  old_keywords - new_keywords
            deletions =  new_keywords - old_keywords
            tk['additions'] = list(additions)
            tk['deletions'] = list(deletions)
            # set keywords dict
            diff['keywords'] = tk


        ret = super(JobViewSet, self).perform_update(serializer)

        # if we get this far, then save the modification

        if len(diff.keys()) > 0:
            # serialize the text
            diff_text = json.dumps(diff)
            
            modification = JobModification(
                changes=diff_text,
                job=instance,
                modified_by=self.request.user,
                modified_date=now
            )

            modification.save()


        return ret


class ActiveJobViewSet(viewsets.ModelViewSet):
    """
    API endpoint for active jobs of the current user
    """
    serializer_class = JobSerializer
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = Job.objects.filter(assigned_worker=self.request.user).exclude(
            archived_date__isnull=False)
        return qs


class UpdateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Job Updates to be viewed or edited.
    """
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint for the Users that are clients
    """
    queryset = User.objects.filter(groups__name='capture_client')
    serializer_class = ClientSerializer
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.created_by = self.request.user
        serializer.created_date = timezone.now()
        instance = serializer.save()

        
        g = Group.objects.get(name='capture_client') 
        instance.groups.add(g)

        # create auth token for the user
        Token.objects.get_or_create(user=instance)

        instance.save()


class WorkerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing workers
    """
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, TokenAuthentication)
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

        return Response(result.values())

    def run_query(self, request, query, params=None):
        cursor = connection.cursor()
        cursor.execute(query, params)

        result = self.serialize(cursor, 60)

        cursor.close()

        return result

    def list(self, request, format=None):
        query = """
        select
            j.id as job_id,
            from_unixtime(FLOOR(unix_timestamp(date)/60)*60) as date,
            FLOOR(unix_timestamp(date)/60)*60 as unixdate, sum(count) as cnt,
            round(avg(count),1) as average
        from capture.main_update
        inner join capture.main_job j on j.id = job_id
        where
            ISNULL(j.archived_date) and
            date > DATE_SUB(utc_timestamp(), INTERVAL 1 HOUR)
        group by j.id, unixdate;
        """
        return self.run_query(request, query)

    def retrieve(self, request, pk=None, format=None):
        query = """
        select
            job_id,
            from_unixtime(FLOOR(unix_timestamp(date)/60)*60) as date,
            FLOOR(unix_timestamp(date)/60)*60 as unixdate,
            sum(count) as cnt,
            round(avg(count),1) as average
        from capture.main_update
        where
            job_id = %s and
            date > DATE_SUB(utc_timestamp(), INTERVAL 1 HOUR)
        group by unixdate;
        """
        return self.run_query(request, query, [pk])


#    def retrieve(self, request, pk=None):
#        pass


class JobModificationViewSet(viewsets.ModelViewSet):
    """
    Job Modification View
    """

    queryset = JobModification.objects.all()
    serializer_class = JobModificationSerializer
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    filter_fields = (
            'id', 'job', 'modified_by')



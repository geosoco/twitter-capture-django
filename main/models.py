import os
import logging
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver

from base.models import FullAuditModel, ModifiedByMixin
from worker.models import Worker
from datetime import datetime


# Get an instance of a logger
logger = logging.getLogger(__name__)


#
# classes
#


class Job(FullAuditModel):
    """
        Model for a capture
    """
    STATUS_UNKNOWN = 0
    STATUS_CREATED = 1
    STATUS_STARTING = 2
    STATUS_STARTED = 3
    STATUS_STOPPING = 4
    STATUS_STOPPED = 5


    STATUS_CHOICES = (
        (STATUS_UNKNOWN, 'unknown'),
        (STATUS_CREATED, 'created'),
        (STATUS_STARTING, 'starting'),
        (STATUS_STARTED, 'started'),
        (STATUS_STOPPING, 'stopping'),
        (STATUS_STOPPED, 'stopped'),
    )

    alphanumeric_start = RegexValidator(regex='^[0-9a-zA-Z_\-\ ]+', message='Must start with an alphanumeric character', code='alpha_start')
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z_\-\ ]*$', 'Only alphanumeric characters, spaces, and _ and - are allowed.')


    name = models.CharField(max_length=64, blank=False, null=False, validators=[alphanumeric,alphanumeric_start], unique=True, 
        help_text="A unique name for this capture. Can only contain alpha-numeric characters, spaces, dashes (-), and underscores (_). ")
    description = models.TextField(
        help_text="A detailed description of the event. Please add possible rumors to this as the event unfolds.",
        null=True)

    keywords = models.TextField(
        help_text="A comma separated list of terms. eg. term1, term2, term3",
        null=True)

    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_CREATED)

    task_id = models.IntegerField(null=True, blank=True)

    first_started = models.DateTimeField(null=True, blank=True)
    started = models.DateTimeField(null=True, blank=True)
    stopped = models.DateTimeField(null=True, blank=True)

    archived_date = models.DateTimeField(null=True, blank=True)
    archived_by = models.ForeignKey(User, null=True, blank=True, default=None, related_name='job_archived_by')

    total_count = models.IntegerField(null=True, blank=True)
    rate = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    ping_date = models.DateTimeField(null=True, blank=True)

    assigned_worker = models.ForeignKey(
        User, null=True, blank=True, default=None,
        related_name='job_assigned_worker',
        help_text="This list will only display unassigned capture clients. If there are none, you must archive an existing capture.")

    def get_absolute_url(self):
        return reverse('capture-details', kwargs={'pk': self.pk, })


@receiver(pre_save, sender=Job)
def on_job_pre_save(sender, instance, *args, **kwargs):
    if instance.id:
        old_job = Job.objects.get(pk=instance.id)

        # if we're archiving it, stop it
        if instance.archived_date is not None and old_job.archived_date != instance.archived_date:
            instance.status = Job.STATUS_STOPPED


        # has the status changed?
        if old_job.status != instance.status:
            # if status is changing
            if instance.status == Job.STATUS_STARTED:
                # first started
                if instance.first_started == None:
                    instance.first_started = datetime.now()
                # now any start value
                instance.started = datetime.now()
            elif instance.status == Job.STATUS_STOPPED:
                instance.stopped = datetime.now()

        # 




class JobModification(ModifiedByMixin):
    """
        Model for change history of a capturejob 
    """
    changes = models.TextField()

    job = models.ForeignKey(Job, blank=True)



class Update(models.Model):
    """
        Model for capture update / update 
    """
    job = models.ForeignKey(Job)
    date = models.DateTimeField(auto_now_add=True)

    count = models.IntegerField(null=True, blank=True)
    total_count = models.IntegerField(null=True, blank=True)
    rate = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)


class LogMessage(models.Model):
    """
        Model for log messages from client
    """
    job = models.ForeignKey(Job)
    date = models.DateTimeField(auto_now_add=True)

    source = models.CharField(max_length=32, blank=True, null=True)
    kind = models.CharField(max_length=4, blank=True, null=True)
    message = models.TextField()







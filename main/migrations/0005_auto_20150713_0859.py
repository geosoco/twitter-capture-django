# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_auto_20150420_0452'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='archived_by',
            field=models.ForeignKey(related_name='job_archived_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='assigned_worker',
            field=models.ForeignKey(related_name='job_assigned_worker', default=None, blank=True, to=settings.AUTH_USER_MODEL, help_text=b'This list will only display unassigned capture clients. If there are none, you must archive an existing capture.', null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='deleted_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.TextField(help_text=b'A detailed description of the event. Please add possible rumors to this as the event unfolds.'),
        ),
        migrations.AlterField(
            model_name='job',
            name='name',
            field=models.CharField(help_text=b'A unique name for this capture. Can only contain alpha-numeric characters, spaces, dashes (-), and underscores (_). ', unique=True, max_length=64, validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z_\\-\\ ]*$', b'Only alphanumeric characters, spaces, and _ and - are allowed.'), django.core.validators.RegexValidator(regex=b'^[0-9a-zA-Z_\\-\\ ]+', message=b'Must start with an alphanumeric character', code=b'alpha_start')]),
        ),
        migrations.AlterField(
            model_name='job',
            name='twitter_keywords',
            field=models.TextField(help_text=b'A comma separated list of terms. eg. term1, term2, term3'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_date', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('twitter_keywords', models.TextField()),
                ('status', models.IntegerField(default=1, choices=[(0, b'unknown'), (1, b'created'), (2, b'starting'), (3, b'started'), (4, b'stopping'), (5, b'stopped')])),
                ('task_id', models.IntegerField(null=True, blank=True)),
                ('first_started', models.DateTimeField(null=True, blank=True)),
                ('started', models.DateTimeField(null=True, blank=True)),
                ('stopped', models.DateTimeField(null=True, blank=True)),
                ('assigned_worker', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('created_by', models.ForeignKey(related_name='job_created_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('deleted_by', models.ForeignKey(related_name='job_deleted_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='job_modified_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JobModification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('changes', models.TextField()),
                ('job', models.ForeignKey(to='main.Job', blank=True)),
                ('modified_by', models.ForeignKey(related_name='jobmodification_modified_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('count', models.IntegerField(null=True, blank=True)),
                ('total_count', models.IntegerField(null=True, blank=True)),
                ('rate', models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)),
                ('job', models.ForeignKey(to='main.Job')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

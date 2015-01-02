# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_auto_20150102_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('twitter_keywords', models.TextField()),
                ('status', models.IntegerField(default=1, choices=[(0, b'unknown'), (1, b'created'), (2, b'starting'), (3, b'started'), (4, b'stopping'), (5, b'stopped'), (6, b'unresponsive'), (7, b'dead')])),
                ('task_id', models.IntegerField(null=True, blank=True)),
                ('first_started', models.DateTimeField(null=True, blank=True)),
                ('started', models.DateTimeField(null=True, blank=True)),
                ('stopped', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JobModification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('changes', models.TextField()),
                ('modification_date', models.DateTimeField(auto_now_add=True)),
                ('job', models.ForeignKey(to='main.Job', blank=True)),
                ('modified_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='CaptureUpdate',
            new_name='Update',
        ),
        migrations.RemoveField(
            model_name='capturejob',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='capturejobmodification',
            name='job',
        ),
        migrations.DeleteModel(
            name='CaptureJob',
        ),
        migrations.RemoveField(
            model_name='capturejobmodification',
            name='modified_by',
        ),
        migrations.DeleteModel(
            name='CaptureJobModification',
        ),
        migrations.AddField(
            model_name='job',
            name='assigned_worker',
            field=models.ForeignKey(to='main.Worker', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='created_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]

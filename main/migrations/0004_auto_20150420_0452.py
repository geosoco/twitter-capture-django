# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150119_2048'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('source', models.CharField(max_length=32, null=True, blank=True)),
                ('kind', models.CharField(max_length=4, null=True, blank=True)),
                ('message', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='archived_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='job',
            name='ping_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='job',
            name='rate',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True),
        ),
        migrations.AddField(
            model_name='job',
            name='total_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='logmessage',
            name='job',
            field=models.ForeignKey(to='main.Job'),
        ),
    ]

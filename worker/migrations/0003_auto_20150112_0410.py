# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('worker', '0002_auto_20150102_2316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worker',
            name='name',
        ),
        migrations.AddField(
            model_name='worker',
            name='last_update',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='worker',
            name='user',
            field=models.ForeignKey(default=8, to=settings.AUTH_USER_MODEL, unique=True),
            preserve_default=False,
        ),
    ]

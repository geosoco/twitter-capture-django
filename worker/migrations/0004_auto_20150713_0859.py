# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0003_auto_20150112_0410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='deleted_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]

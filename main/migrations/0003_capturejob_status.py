# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20141013_0338'),
    ]

    operations = [
        migrations.AddField(
            model_name='capturejob',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'created'), (1, b'started'), (2, b'stopped')]),
            preserve_default=True,
        ),
    ]

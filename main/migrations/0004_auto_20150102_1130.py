# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_capturejob_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capturejob',
            name='status',
            field=models.IntegerField(default=1, choices=[(0, b'unknown'), (1, b'created'), (2, b'starting'), (3, b'started'), (4, b'stopping'), (5, b'stopped'), (6, b'unresponsive'), (7, b'dead')]),
            preserve_default=True,
        ),
    ]

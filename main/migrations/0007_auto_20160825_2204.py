# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20160811_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.TextField(help_text=b'A detailed description of the event. Please add possible rumors to this as the event unfolds.', null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='keywords',
            field=models.TextField(help_text=b'A comma separated list of terms. eg. term1, term2, term3', null=True),
        ),
    ]

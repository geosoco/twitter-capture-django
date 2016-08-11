# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20150713_0859'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='twitter_keywords',
            new_name='keywords',
        ),
    ]

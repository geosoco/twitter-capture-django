# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='name',
            field=models.CharField(unique=True, max_length=64, validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z_\\-\\ ]*$', b'Only alphanumeric characters, spaces, and _ and - are allowed.')]),
            preserve_default=True,
        ),
    ]

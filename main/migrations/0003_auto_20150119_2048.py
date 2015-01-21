# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150119_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='name',
            field=models.CharField(unique=True, max_length=64, validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z_\\-\\ ]*$', b'Only alphanumeric characters, spaces, and _ and - are allowed.'), django.core.validators.RegexValidator(regex=b'^[0-9a-zA-Z_\\-\\ ]+', message=b'Must start with an alphanumeric character', code=b'alpha_start')]),
            preserve_default=True,
        ),
    ]

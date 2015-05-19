# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_reportphoto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='photo',
        ),
    ]

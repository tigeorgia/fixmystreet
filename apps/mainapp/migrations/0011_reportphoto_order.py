# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_reportphoto'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportphoto',
            name='order',
            field=models.IntegerField(default=0, verbose_name='order', blank=True),
            preserve_default=False,
        ),
    ]

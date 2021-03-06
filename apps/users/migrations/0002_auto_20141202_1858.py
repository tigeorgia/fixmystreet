# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fmsuser',
            name='username',
            field=models.CharField(max_length=20, verbose_name='username'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fmsuser',
            name='phone',
            field=models.CharField(default='', max_length=255, verbose_name='phone'),
            preserve_default=False,
        ),
    ]

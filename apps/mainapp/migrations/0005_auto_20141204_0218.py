# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20141202_2154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='is_confirmed',
        ),
        migrations.RemoveField(
            model_name='report',
            name='is_hate',
        ),
        migrations.RemoveField(
            model_name='reportupdate',
            name='author',
        ),
        migrations.RemoveField(
            model_name='reportupdate',
            name='confirm_token',
        ),
        migrations.RemoveField(
            model_name='reportupdate',
            name='first_update',
        ),
        migrations.RemoveField(
            model_name='reportupdate',
            name='is_confirmed',
        ),
        migrations.RemoveField(
            model_name='reportupdate',
            name='is_verified_author',
        ),
        migrations.RemoveField(
            model_name='reportupdate',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='reportupdate',
            name='email',
        ),
        migrations.AddField(
            model_name='report',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reportupdate',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]

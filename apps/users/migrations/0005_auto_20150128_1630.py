# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_fmspasswordresettoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fmspasswordresettoken',
            name='id',
        ),
        migrations.RemoveField(
            model_name='fmsusertoken',
            name='id',
        ),
        migrations.AddField(
            model_name='fmspasswordresettoken',
            name='used_ip',
            field=models.GenericIPAddressField(help_text=b'IP of request which used the token', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fmspasswordresettoken',
            name='token',
            field=models.CharField(max_length=40, unique=True, serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fmsusertoken',
            name='token',
            field=models.CharField(max_length=40, unique=True, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]

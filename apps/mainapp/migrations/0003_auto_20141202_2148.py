# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0002_auto_20141202_2145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='author',
        ),
        migrations.AddField(
            model_name='report',
            name='user',
            field=models.ForeignKey(related_name='reports', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reportupdate',
            name='user',
            field=models.ForeignKey(related_name='report_updates', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

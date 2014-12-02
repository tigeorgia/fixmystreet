# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import stdimage.models

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='photo',
            field=stdimage.models.StdImageField(upload_to=b'photos', verbose_name='* Photo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reportupdate',
            name='photo',
            field=stdimage.models.StdImageField(upload_to=b'photos/updates', verbose_name='* Photo', blank=True),
            preserve_default=True,
        ),
    ]

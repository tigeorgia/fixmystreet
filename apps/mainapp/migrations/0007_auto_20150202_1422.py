# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20141207_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ward',
            name='councillor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]

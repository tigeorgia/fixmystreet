# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20150128_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fmssettings',
            name='user',
            field=models.OneToOneField(related_name='user_settings', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]

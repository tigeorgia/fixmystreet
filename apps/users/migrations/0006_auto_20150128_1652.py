# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20150128_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fmspasswordresettoken',
            name='user',
            field=models.ForeignKey(related_name='password_reset_token', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]

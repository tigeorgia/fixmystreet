# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20141215_0348'),
    ]

    operations = [
        migrations.CreateModel(
            name='FMSPasswordResetToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=40)),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='created at')),
                ('ip', models.GenericIPAddressField(null=True)),
                ('used', models.BooleanField(default=False)),
                ('user', models.OneToOneField(related_name='password_reset_token', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

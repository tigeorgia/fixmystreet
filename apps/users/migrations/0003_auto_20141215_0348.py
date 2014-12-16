# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20141202_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='FMSUserToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=40)),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='created at')),
                ('user', models.OneToOneField(related_name='fms_user_token', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fmsuser',
            name='is_confirmed',
            field=models.BooleanField(default=False, verbose_name='email confirmed'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fmsuser',
            name='is_councillor',
            field=models.BooleanField(default=False, verbose_name='councillor'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20150201_0301'),
    ]

    operations = [
        migrations.CreateModel(
            name='FMSUserAuthToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=255, verbose_name='token')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('user', models.OneToOneField(related_name='auth_token', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FMSUserTempToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=255, verbose_name='token')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('ip', models.GenericIPAddressField(null=True)),
                ('used', models.BooleanField(default=False)),
                ('used_ip', models.GenericIPAddressField(help_text=b'IP of request which used the token', null=True)),
                ('user', models.ForeignKey(related_name='temp_token', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='FMSSettings',
            new_name='FMSUserSettings',
        ),
        migrations.RemoveField(
            model_name='fmspasswordresettoken',
            name='user',
        ),
        migrations.DeleteModel(
            name='FMSPasswordResetToken',
        ),
        migrations.RemoveField(
            model_name='fmsusertoken',
            name='user',
        ),
        migrations.DeleteModel(
            name='FMSUserToken',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChemikuchaUser',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('api_read', models.BooleanField(default=False)),
                ('api_write', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='apiuser',
            name='user',
        ),
        migrations.DeleteModel(
            name='ApiUser',
        ),
    ]

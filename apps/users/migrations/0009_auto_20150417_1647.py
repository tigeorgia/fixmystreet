# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import os
import binascii

def generate_new_auth_tokens(apps, schema_editor):
    User = apps.get_model('users', 'FMSUser')
    AuthToken = apps.get_model('users', 'FMSUserAuthToken')
    users = User.objects.all()
    for user in users:
        AuthToken.objects.create(user=user, token=binascii.hexlify(os.urandom(20)).decode())

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20150417_1646'),
    ]

    operations = [
        migrations.RunPython(generate_new_auth_tokens),
    ]

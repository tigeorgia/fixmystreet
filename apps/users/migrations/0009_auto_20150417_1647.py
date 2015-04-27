# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20150417_1646'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='fmsuserauthtoken',
            table='users_fmsuser_auth_token',
        ),
        migrations.AlterModelTable(
            name='fmsusersettings',
            table='users_fmsuser_settings',
        ),
        migrations.AlterModelTable(
            name='fmsusertemptoken',
            table='users_fmsuser_temp_token',
        ),
    ]

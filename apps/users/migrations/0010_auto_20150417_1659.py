# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20150417_1647'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='fmsuser',
            table='users_fms_user',
        ),
        migrations.AlterModelTable(
            name='fmsuserauthtoken',
            table='users_fms_user_auth_token',
        ),
        migrations.AlterModelTable(
            name='fmsusersettings',
            table='users_fms_user_settings',
        ),
        migrations.AlterModelTable(
            name='fmsusertemptoken',
            table='users_fms_user_temp_token',
        ),
    ]

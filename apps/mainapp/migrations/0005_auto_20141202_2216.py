# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def update_reports(apps, schema_editor):
    Report = apps.get_model('mainapp', 'Report')
    ReportUpdate = apps.get_model('mainapp', 'ReportUpdate')
    FrozenUser = apps.get_model('users', 'FMSUser')

    for report_update in ReportUpdate.objects.filter(is_confirmed=True):
        email = report_update.email.lower()
        frozen_user = FrozenUser.objects.get(email=email)
        report_update.user = frozen_user

        if report_update.first_update:
            report_update.report.user = frozen_user
            report_update.report.save()

        report_update.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0004_auto_20141202_2154'),
    ]

    operations = [
        migrations.RunPython(update_reports),
    ]

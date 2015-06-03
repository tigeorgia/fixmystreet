# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def delete_old_updates(apps, schema_editor):
    """
    Before migrating to user system, first report update was source for report description
    This is no longer the case, but those first updates are still kept in the database
    and are excluded from the view in quite an ugly way.
    This function checks if descriptions of report update and report are the same and removes the update
    """
    Report = apps.get_model('mainapp', 'Report')
    ReportUpdate = apps.get_model('mainapp', 'ReportUpdate')

    for update in ReportUpdate.objects.all():
        report = update.report
        # If update description and the day of creation are the same,
        # there's 99.9% chance, this update is redundant and should be removed
        if update.desc == report.desc and update.created_at.day == report.created_at.day:
            update.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_auto_20150525_1233'),
    ]

    operations = [
        migrations.RunPython(delete_old_updates)
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_previous_report(apps, schema_editor):
    ReportUpdate = apps.get_model('mainapp', 'ReportUpdate')

    for update in ReportUpdate.objects.values('id', 'created_at', 'report__id'):
        try:
            prev_update = ReportUpdate.objects.filter(
                created_at__lt=update['created_at'], report_id=update['report__id']
            ).order_by('-created_at')[0]
        except IndexError:
            continue

        # We want to avoid Model.save() method since
        # it does a lot more than save. (signals, modified date etc.)
        # update() method dos not do anything except of well, updating.
        # but is available only to QuerySets.
        ReportUpdate.objects.filter(id=update['id']).update(prev_update=prev_update)


class Migration(migrations.Migration):
    dependencies = [
        ('mainapp', '0015_auto_20150603_1745'),
    ]

    operations = [
        migrations.RunPython(add_previous_report)
    ]

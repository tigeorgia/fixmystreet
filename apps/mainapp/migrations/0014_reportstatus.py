# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

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
        if update.desc == update.report.desc:
            update.delete()


def update_statuses(apps, schema_editor):
    Report = apps.get_model('mainapp', 'Report')
    ReportUpdate = apps.get_model('mainapp', 'ReportUpdate')
    ReportStatus = apps.get_model('mainapp', 'ReportStatus')

    for report in Report.objects.all():
        report_updates = ReportUpdate.objects.filter(report_id=report.id).order_by('created_at')
        if report_updates:
            previous_update = None
            for update in report_updates:
                # If previous update is not present, it means
                # this is the first update, and it's always 'not-fixed'
                if not previous_update:
                    if update.status != 'not-fixed':
                        rep_status = ReportStatus(created_at=update.created_at, report_id=update.report.id, status=update.status,
                                              user_id=update.user.id)
                        rep_status.save()
                elif previous_update:
                    rep_status = ReportStatus(created_at=update.created_at, report_id=update.report.id, status=update.status,
                                              user_id=update.user.id)
                    rep_status.save()

                previous_update = update


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0013_auto_20150525_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'not-fixed', help_text='Report status', max_length=32, verbose_name='status', choices=[(b'not-fixed', 'Not Fixed'), (b'fixed', 'Fixed'), (b'in-progress', 'In Progress')])),
                ('created_at', models.DateTimeField(help_text='Date when report was created',)),
                ('report', models.ForeignKey(related_name='report_statuses', verbose_name='report', to='mainapp.Report')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL, help_text='creator of status')),
            ],
        ),
        migrations.RunPython(delete_old_updates),
        migrations.RunPython(update_statuses)
    ]

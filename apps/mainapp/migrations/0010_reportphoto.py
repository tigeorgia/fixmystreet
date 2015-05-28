# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import stdimage.models


def migrate_photos(apps, schema_editor):
    """
    Migrate report photos from Report model to ReportPhoto model
    and link report model from there
    """
    Report = apps.get_model('mainapp', 'Report')
    ReportPhoto = apps.get_model('mainapp', 'ReportPhoto')

    for report in Report.objects.all().exclude(photo__isnull=True).exclude(photo=""):
        photo = ReportPhoto(report=report, photo=report.photo)
        photo.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_auto_20150427_0155'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', stdimage.models.StdImageField(help_text='Report photo', upload_to=b'photos', verbose_name='photo', blank=True)),
                ('report', models.ForeignKey(related_name='report_photos', to='mainapp.Report')),
            ],
        ),
        migrations.RunPython(migrate_photos),
    ]

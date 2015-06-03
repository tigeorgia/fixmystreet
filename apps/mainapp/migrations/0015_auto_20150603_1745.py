# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import stdimage.models
import stdimage.utils


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_remove_report_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportUpdatePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(verbose_name='order')),
                ('photo', stdimage.models.StdImageField(help_text='Report update photo', upload_to=stdimage.utils.UploadToUUID(path=b'photos/updates'), verbose_name='photo')),
            ],
        ),
        migrations.AddField(
            model_name='reportupdate',
            name='prev_update',
            field=models.ForeignKey(related_name='next_update', verbose_name='previous update', to='mainapp.ReportUpdate', help_text='Link to the previous report update', null=True),
        ),
        migrations.AddField(
            model_name='reportupdatephoto',
            name='report_update',
            field=models.ForeignKey(related_name='update_photos', to='mainapp.ReportUpdate'),
        ),
    ]

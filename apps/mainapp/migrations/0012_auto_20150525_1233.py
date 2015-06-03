# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.core.management import call_command
from stdimage import StdImageField
from stdimage.utils import UploadToUUID
import os

def remove_old_photos():
    photo_root = os.path.join(settings.MEDIA_ROOT, 'photos')
    files = [f for f in os.listdir(photo_root) if os.path.isfile(os.path.join(photo_root, f))]
    keys_to_remove = ['thumbnail', 'large', 'size', 'photo', '_']
    for file in files:
        if any(key in file for key in keys_to_remove):
            file_absolute = os.path.join(photo_root, file)
            os.remove(file_absolute)


def rename_photos(apps, schema_editor):
    ReportPhoto = apps.get_model('mainapp', 'ReportPhoto')

    for rep_photo in ReportPhoto.objects.all():
        old_photo = rep_photo.photo
        try:
            rep_photo.photo = old_photo.file
            rep_photo.save()
        except IOError:
            pass

    remove_old_photos()


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_reportphoto_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportphoto',
            name='order',
            field=models.IntegerField(verbose_name='order'),
        ),
        migrations.AlterField(
            model_name='reportphoto',
            name='photo',
            field=StdImageField(help_text='Report photo', upload_to=UploadToUUID(path=b'photos'), verbose_name='photo'),
        ),
        migrations.RunPython(rename_photos)
    ]

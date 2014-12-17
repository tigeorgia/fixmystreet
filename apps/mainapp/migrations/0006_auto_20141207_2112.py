# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20141204_0218'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='reportupdate',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterField(
            model_name='report',
            name='category',
            field=models.ForeignKey(verbose_name='category', to='mainapp.ReportCategory', help_text='Report category'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='created_at',
            field=models.DateTimeField(help_text='Date when report was created', auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='desc',
            field=models.TextField(help_text='Report description', verbose_name='details'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='fixed_at',
            field=models.DateTimeField(help_text='Date when report was fixed', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='photo',
            field=stdimage.models.StdImageField(upload_to=b'photos', verbose_name='photo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='sent_at',
            field=models.DateTimeField(help_text='Date when report was sent to city representative', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='status',
            field=models.CharField(default=b'not-fixed', help_text='Report status', max_length=32, verbose_name='status', choices=[(b'not-fixed', 'Not Fixed'), (b'fixed', 'Fixed'), (b'in-progress', 'In Progress')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='street',
            field=models.CharField(help_text=b'Address of the problem', max_length=255, verbose_name='street address'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='title',
            field=models.CharField(help_text='Report title', max_length=100, verbose_name='title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='updated_at',
            field=models.DateTimeField(help_text='Date when report was updated', auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='user',
            field=models.ForeignKey(related_name='reports', to=settings.AUTH_USER_MODEL, help_text='Author of the report'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='ward',
            field=models.ForeignKey(verbose_name='ward', to='mainapp.Ward', help_text='Ward associated with report'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='photo',
            field=stdimage.models.StdImageField(help_text='Please upload report photo', upload_to=b'photos', verbose_name='photo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reportsubscriber',
            name='report',
            field=models.ForeignKey(related_name='subscribers', to='mainapp.Report'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reportupdate',
            name='desc',
            field=models.TextField(verbose_name='details'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reportupdate',
            name='photo',
            field=stdimage.models.StdImageField(upload_to=b'photos/updates', verbose_name='photo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reportupdate',
            name='status',
            field=models.CharField(default=b'not-fixed', max_length=32, verbose_name='status', choices=[(b'not-fixed', 'Not Fixed'), (b'fixed', 'Fixed'), (b'in-progress', 'In Progress')]),
            preserve_default=True,
        ),
    ]

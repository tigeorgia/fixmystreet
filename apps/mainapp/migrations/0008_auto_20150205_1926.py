# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_auto_20150202_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='email_sent_to',
            field=models.EmailField(max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='fixed_at',
            field=models.DateTimeField(help_text='Date when report was fixed', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='ip',
            field=models.GenericIPAddressField(null=True, blank=True),
            preserve_default=True,
        ),
    ]

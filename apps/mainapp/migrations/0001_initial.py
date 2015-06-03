# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from stdimage import StdImageField
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_en', models.CharField(max_length=100, null=True, verbose_name='Name', blank=True)),
                ('name_ka', models.CharField(max_length=100, verbose_name='Name')),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
            ],
            options={
                'db_table': 'cities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Councillor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name_en', models.CharField(max_length=100, null=True, verbose_name='First name', blank=True)),
                ('first_name_ka', models.CharField(max_length=100, verbose_name='First name')),
                ('last_name_en', models.CharField(max_length=100, null=True, verbose_name='Last name', blank=True)),
                ('last_name_ka', models.CharField(max_length=100, verbose_name='Last name')),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('fax', models.CharField(max_length=20, null=True, blank=True)),
                ('phone', models.CharField(max_length=20, null=True, blank=True)),
            ],
            options={
                'db_table': 'councillors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rule', models.IntegerField(choices=[(0, b'Send Reports to Councillor Email Address'), (1, b'Send Reports Matching Category Class (eg. Parks) To This Email'), (2, b'Send Reports Not Matching Category Class To This Email')])),
                ('is_cc', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FaqEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('q_en', models.CharField(max_length=100, null=True, blank=True)),
                ('q_ka', models.CharField(max_length=100)),
                ('a_en', models.TextField(null=True, blank=True)),
                ('a_ka', models.TextField(null=True, blank=True)),
                ('slug', models.SlugField(null=True, blank=True)),
                ('order', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'faq_entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PollingStation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('ward_number', models.IntegerField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True)),
                ('city', models.ForeignKey(to='mainapp.City')),
            ],
            options={
                'db_table': 'polling_stations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_en', models.CharField(max_length=100, null=True, verbose_name='Name', blank=True)),
                ('name_ka', models.CharField(max_length=100, verbose_name='Name')),
                ('abbrev', models.CharField(max_length=3)),
            ],
            options={
                'db_table': 'province',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='Subject')),
                ('ip', models.GenericIPAddressField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('street', models.CharField(max_length=255, verbose_name='Street address')),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('fixed_at', models.DateTimeField(null=True)),
                ('status', models.CharField(default=b'not-fixed', max_length=32, verbose_name='Status', choices=[(b'not-fixed', 'Not Fixed'), (b'fixed', 'Fixed'), (b'in-progress', 'In Progress')])),
                ('is_hate', models.BooleanField(default=False)),
                ('sent_at', models.DateTimeField(null=True)),
                ('email_sent_to', models.EmailField(max_length=75, null=True)),
                ('reminded_at', models.DateTimeField(auto_now_add=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True)),
                ('photo', StdImageField(upload_to=b'photos', verbose_name='* Photo', blank=True)),
                ('desc', models.TextField(null=True, verbose_name='Details', blank=True)),
                ('author', models.CharField(max_length=255, verbose_name='Name')),
                ('is_confirmed', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'reports',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReportCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_en', models.CharField(max_length=100, null=True, verbose_name='Title', blank=True)),
                ('name_ka', models.CharField(max_length=100, verbose_name='Title')),
                ('hint_en', models.TextField(null=True, verbose_name='Hint', blank=True)),
                ('hint_ka', models.TextField(null=True, verbose_name='Hint', blank=True)),
            ],
            options={
                'db_table': 'report_categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReportCategoryClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_en', models.CharField(max_length=100, null=True, verbose_name='Title', blank=True)),
                ('name_ka', models.CharField(max_length=100, verbose_name='Title')),
            ],
            options={
                'db_table': 'report_category_classes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReportSubscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('confirm_token', models.CharField(max_length=255, null=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=75, verbose_name='Email')),
                ('report', models.ForeignKey(to='mainapp.Report')),
            ],
            options={
                'db_table': 'report_subscribers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReportUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desc', models.TextField(null=True, verbose_name='Details', blank=True)),
                ('ip', models.GenericIPAddressField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('status', models.CharField(default=b'not-fixed', max_length=32, verbose_name='Status', choices=[(b'not-fixed', 'Not Fixed'), (b'fixed', 'Fixed'), (b'in-progress', 'In Progress')])),
                ('is_verified_author', models.BooleanField(default=False)),
                ('confirm_token', models.CharField(max_length=255, null=True)),
                ('email', models.EmailField(max_length=255, verbose_name='Email')),
                ('author', models.CharField(max_length=255, verbose_name='Name')),
                ('phone', models.CharField(max_length=255, verbose_name='Phone')),
                ('first_update', models.BooleanField(default=False)),
                ('photo', StdImageField(upload_to=b'photos/updates', verbose_name='* Photo', blank=True)),
                ('report', models.ForeignKey(to='mainapp.Report')),
            ],
            options={
                'db_table': 'report_updates',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VerifiedAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(max_length=255, verbose_name='Domain')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_en', models.CharField(max_length=100, null=True, verbose_name='Name', blank=True)),
                ('name_ka', models.CharField(max_length=100, verbose_name='Name')),
                ('number', models.IntegerField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True)),
                ('city', models.ForeignKey(to='mainapp.City')),
                ('councillor', models.ForeignKey(to='mainapp.Councillor')),
            ],
            options={
                'db_table': 'wards',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='reportcategory',
            name='category_class',
            field=models.ForeignKey(to='mainapp.ReportCategoryClass'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='category',
            field=models.ForeignKey(verbose_name='Category', to='mainapp.ReportCategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='ward',
            field=models.ForeignKey(verbose_name='Ward', to='mainapp.Ward', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailrule',
            name='category',
            field=models.ForeignKey(blank=True, to='mainapp.ReportCategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailrule',
            name='category_class',
            field=models.ForeignKey(blank=True, to='mainapp.ReportCategoryClass', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailrule',
            name='city',
            field=models.ForeignKey(to='mainapp.City'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(to='mainapp.Province'),
            preserve_default=True,
        ),
    ]

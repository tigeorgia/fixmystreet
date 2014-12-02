# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from apps.users.models import FMSUser
from django.core.exceptions import ObjectDoesNotExist


def _get_first_last_name(name):
    """
    Accepts full name and returns first, last name tuple, or name and empty last name
    @param name: Full name
    @type name: str
    @return: (first, last)
    @rtype: tuple
    """
    names = name.rstrip().split(' ')
    filtered_names = filter(None, names)
    first_name = filtered_names[0]
    try:
        last_name = filtered_names[1]
    except IndexError:
        last_name = ''
    return (first_name, last_name)


def _create_user(apps, report_update):
    FrozenUser = apps.get_model('users', 'FMSUser')
    email = report_update.email.lower()
    password = FMSUser.objects.make_random_password()
    first_name, last_name = _get_first_last_name(report_update.author)
    email_username = report_update.email.split('@')[0]
    # Allow only alphanumeric and underscore
    username = ''.join(c for c in email_username if c.isalnum() or c is '_')[:20]
    fms_user = FMSUser.objects.create_user(username=username, email=email, password=password)
    print username

    frozen_user = FrozenUser.objects.get(email=email)
    return frozen_user


def create_users(apps, schema_editor):
    Report = apps.get_model('mainapp', 'Report')
    ReportUpdate = apps.get_model('mainapp', 'ReportUpdate')
    FrozenUser = apps.get_model('users', 'FMSUser')

    for report_update in ReportUpdate.objects.filter(is_confirmed=True):
        email = report_update.email.lower()
        try:
            frozen_user = FrozenUser.objects.get(email=email)
        except ObjectDoesNotExist:
            frozen_user = _create_user(apps, report_update)

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0003_auto_20141202_2148'),
    ]

    operations = [
        migrations.RunPython(create_users),
    ]

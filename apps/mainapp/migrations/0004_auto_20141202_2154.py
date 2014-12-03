# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from apps.users.models import FMSUser
from django.core.exceptions import ObjectDoesNotExist
import random
import time
import sys


def _remove_not_confirmed_updates(ReportUpdate):
        """
        Remove old-style reports (i.e. reports without users)
        """

        updates = ReportUpdate.objects.filter(is_confirmed=False)
        print "\n{0} ReportUpdate objects to remove".format(updates.count())
        time.sleep(3)

        for update in updates:
            report = update.report
            update.delete()

            # Remove report instance if it has no updates left
            if not report.report_updates.all():
                report.delete()


def _remove_not_confirmed_reports(Report):
    """
    Removes leftover unconfirmed reports. This shouldn't bee needed
    though, unless update remover fails to remove all reports.
    """
    reports = Report.objects.filter(is_confirmed=False)
    print "{0} Report objects to remove".format(reports.count())
    time.sleep(3)
    reports.delete()


def _get_first_last_name(name):
    """
    Accepts full name and returns first, last name tuple, or name and empty last name
    @param name: Full name
    @type name: str
    @return: first, last
    @rtype: tuple
    """
    names = name.rstrip().split(' ')
    filtered_names = filter(None, names)
    first_name = filtered_names[0]
    try:
        last_name = filtered_names[1]
    except IndexError:
        last_name = ''
    return first_name, last_name


def _create_user(apps, report_update):
    """
    Create users with real model instead of migration's frozen one
    since frozen model doesn't allow custom manager methods we need.

    @param report_update: ReportUpdate Instance
    @type report_update: ReportUpdate
    @return: Frozen user instance
    @rtype: FMSUser (frozen)
    """
    FrozenUser = apps.get_model('users', 'FMSUser')
    email = report_update.email.lower()
    password = FMSUser.objects.make_random_password()
    first_name, last_name = _get_first_last_name(report_update.author)
    email_username = report_update.email.split('@')[0]
    phone = report_update.phone
    # Allow only alphanumeric and underscore
    username = ''.join(c for c in email_username if c.isalnum() or c is '_')[:20]

    if FMSUser.username_exists(username):
        username += ''.join(random.choice('0123456789') for i in range(2))

    fms_user = FMSUser.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                           last_name=last_name, phone=phone)

    frozen_user = FrozenUser.objects.get(email=email)
    return frozen_user


def remove_old_reports(apps, schema_editor):
    Report = apps.get_model('mainapp', 'Report')
    ReportUpdate = apps.get_model('mainapp', 'ReportUpdate')

    _remove_not_confirmed_updates(ReportUpdate)
    _remove_not_confirmed_reports(Report)


def create_users(apps, schema_editor):
    ReportUpdate = apps.get_model('mainapp', 'ReportUpdate')
    FrozenUser = apps.get_model('users', 'FMSUser')
    updates = ReportUpdate.objects.filter(is_confirmed=True).order_by('email').distinct('email')
    users_total = float(updates.count())
    users_created = 0.0

    for report_update in updates:
        email = report_update.email.lower()
        try:
            frozen_user = FrozenUser.objects.get(email=email)
        except ObjectDoesNotExist:
            frozen_user = _create_user(apps, report_update)

        users_created += 1
        print "Progress: {0:.2f}%, User: {1}.".format(users_created / users_total*100, email)


def update_reports(apps, schema_editor):
    ReportUpdate = apps.get_model('mainapp', 'ReportUpdate')
    FrozenUser = apps.get_model('users', 'FMSUser')

    print "Updating reports...\n"

    for report_update in ReportUpdate.objects.filter(is_confirmed=True):
        report = report_update.report
        email = report_update.email.lower()
        frozen_user = FrozenUser.objects.get(email=email)
        report_update.user = frozen_user
        report_update.updated_at = report_update.created_at
        report.updated_at = report.report_updates.order_by('-created_at').first().created_at

        if report_update.first_update:
            report.user = frozen_user

        report.save()
        report_update.save()


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0003_auto_20141202_2148'),
    ]

    operations = [
        migrations.RunPython(remove_old_reports),
        migrations.RunPython(create_users),
        migrations.RunPython(update_reports),
    ]

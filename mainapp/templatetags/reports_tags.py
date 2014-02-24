# -*- coding: utf-8 -*
from django import template
from django.conf import settings
from mainapp.models import Report
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

register = template.Library()

@register.simple_tag(takes_context=False)
def latest_reports(number=5):
    reports = Report.objects.filter(
        is_confirmed__exact=True
    ).order_by('-created_at')[:number]
    result = ""
    for report in reports:
        result += make_url(report.get_absolute_url(), report.title.encode('utf-8'))
    return "<ul>" + result + '</ul>'


def make_url(absolute, title):
    url = '<li><a href="{0}">{1}</a></li>'.format(absolute, title)
    return url
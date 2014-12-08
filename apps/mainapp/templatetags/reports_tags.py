# -*- coding: utf-8 -*
from django import template

from apps.mainapp.models import Report


register = template.Library()

@register.simple_tag(takes_context=False)
def latest_reports(number=5):
    reports = Report.active.order_by('-created_at')[:number]
    result = ""
    for report in reports:
        result += make_url(report.get_absolute_url(), report.title.encode('utf-8'))
    return "<ul>" + result + '</ul>'


def make_url(absolute, title):
    url = '<li><a href="{0}">{1}</a></li>'.format(absolute, title)
    return url
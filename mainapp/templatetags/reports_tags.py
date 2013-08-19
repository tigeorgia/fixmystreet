# -*- coding: utf-8 -*
from django import template
from django.conf import settings
from mainapp.models import Report
from django.utils.translation import ugettext as _

register = template.Library()

@register.simple_tag(takes_context=True)
def latest_reports(context, number=5):
    lang = context['LANGUAGE_CODE']
    reports = Report.objects.filter(
        is_confirmed__exact=True
    ).order_by('-created_at')[:number]
    header = '<div class="report-updates"><h3>{0}</h3>'.format(_("Recent updates"))
    result = ""
    for report in reports:
        result += make_url(lang, report.get_absolute_url(), report.title.encode('utf-8'))
    return header + "<ul>" + result + '</ul></div>'


def make_url(lang, absolute, title):
    url = '<li><a href="/{0}{1}">{2}</a></li>'.format(lang, absolute, title)
    return url
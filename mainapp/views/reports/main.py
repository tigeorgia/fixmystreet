# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.contrib.gis.geos import *
from django.utils.translation import ugettext as _
from django_filters.views import FilterView

from mainapp.models import Report, ReportUpdate, Ward, FixMyStreetMap, ReportCategory
from mainapp.forms import ReportForm, ReportUpdateForm, sortingForm
from mainapp.filters import ReportFilter
from mainapp.utils import random_image
from utils import utils


def new(request):
    form_error = category_error = title = street = author = email = phone = desc = pnt = city = None

    if request.method == "POST":
        POST = request.POST.copy()

        point_str = "POINT(" + POST['lon'] + " " + POST['lat'] + ")"
        pnt = fromstr(point_str, srid=4326)
        title = POST['title']
        street = POST['street']
        author = POST['author']
        email = POST['email']
        phone = POST['phone']
        desc = POST['desc']
        city = POST['city']

        update_form = ReportUpdateForm(
            data={'email': email, 'desc': desc, 'author': author, 'phone': phone, 'status': 'not-fixed'} or None,
            files=request.FILES or None)
        report_form = ReportForm(data={'title': title, 'street': street} or None, files=request.FILES or None)
        if update_form.is_valid and report_form.is_valid:
            pass
        else:
            HttpResponseRedirect('/')

        if request.POST.get('step') == '2':


            # this is a lot more complicated than it has to be because of the infortmation
            # spread across two records.

            if request.POST['category_id'] != "" and update_form.is_valid() and report_form.is_valid():
                report = report_form.save(commit=False)
                report.point = pnt
                report.category_id = request.POST['category_id']
                report.ip = utils.get_client_ip(request)
                report.author = request.POST['author']
                report.desc = request.POST['desc']
                report.ward = Ward.objects.get(geom__contains=pnt)
                report.save()
                update = update_form.save(commit=False)
                update.report = report
                update.ip = utils.get_client_ip(request)
                update.first_update = True
                update.created_at = report.created_at
                update.save()
                return HttpResponseRedirect(report.get_absolute_url())

                # other form errors are handled by the form objects.
            if not request.POST['category_id']:
                category_error = _("Please select a category")

    else:
        return HttpResponseRedirect('/')

    return render_to_response("reports/new.html",
                              {"lat": pnt.y,
                               "lon": pnt.x,
                               "city": city,
                               "google": FixMyStreetMap(pnt, True),
                               "title": title,
                               "street": street,
                               "author": author,
                               "email": email,
                               "phone": phone,
                               "update_form": update_form,
                               "report_form": report_form,
                               "categories": ReportCategory.objects.all().order_by("category_class"),
                               "category_error": category_error,
                               "form_error": form_error},
                              context_instance=RequestContext(request))


def show(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    subscribers = report.reportsubscriber_set.count() + 1
    return render_to_response("reports/show.html",
                              {"report": report,
                               "subscribers": subscribers,
                               "ward": report.ward,
                               "updates": ReportUpdate.objects.filter(report=report, is_confirmed=True).order_by(
                                   "created_at")[1:],
                               "update_form": ReportUpdateForm(),
                               "google": FixMyStreetMap(report.point)},
                              context_instance=RequestContext(request))


def poster(request, report_id):
    # Build URL
    report = get_object_or_404(Report, id=report_id)
    url = request.get_host() + request.path[:-7]  # Hard-coded value to trim "/poster" off the end. Sorry.
    return render_to_response("reports/poster.html", {'url': url, 'report': report})


class ReportListView(FilterView):
    model = Report
    filterset_class = ReportFilter
    template_name = 'reports/report_list.html'
    template_name_suffix = None
    context_object_name = 'report_list'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        ctx = super(ReportListView, self).get_context_data(**kwargs)
        data = self.request.GET
        today = datetime.datetime.combine(datetime.datetime.today(), datetime.time.max)
        ctx['random_image'] = random_image()
        ctx['sortform'] = sortingForm(data={
            'created_after': data.get('created_after'),
            'created_before': data.get('created_before'),
            'sorting': data.get('sorting', ),
        })
        return ctx

    def get_queryset(self):
        data = self.request.GET
        today = datetime.datetime.combine(datetime.datetime.today(), datetime.time.max)
        form = sortingForm(data={
            'created_after': data.get('created_after') or '1990-01-01',
            'created_before': data.get('created_before') or today,
            'sorting': data.get('sorting') or '-created_at',
        })

        if form.is_valid():
            qs = Report.objects.filter(is_confirmed=True, created_at__range=(
                form.cleaned_data['created_after'], form.cleaned_data['created_before']))
        else:
            qs = Report.objects.filter(is_confirmed=True)

        qs = qs.prefetch_related('ward', 'category').order_by(form.cleaned_data['sorting'])

        qs = qs.extra(
            select={
                'sub_count': 'SELECT COUNT(*)\
                                FROM report_subscribers\
                                WHERE reports.id = report_subscribers.report_id'
            }
        )

        return qs
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from mainapp.models import Report, ReportUpdate, Ward, FixMyStreetMap, ReportCategory, ReportFilter
from mainapp.forms import ReportForm, ReportUpdateForm, sortingForm
from django.template import RequestContext
from django.db.models import Count, connection
from django.contrib.gis.geos import *
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from time import strptime
from utils import utils
import datetime


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

        update_form = ReportUpdateForm({'email': email, 'desc': desc, 'author': author, 'phone': phone}, request.FILES)
        report_form = ReportForm({'title': title, 'street': street}, request.FILES)
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


def report_list(request, extra_content=None):
    template = 'reports/report_filter.html'
    ajax_template = 'reports/report_filter_ajax.html'
    sortform = sortingForm()

    for key in request.GET:
        try:
            sortform.fields[key].initial = request.GET[key]
        except KeyError:
            pass

    sort = request.GET.get('sorting', '-created_at')
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    fromstart = "1990-01-01"
    last_month = (datetime.datetime.today() + datetime.timedelta(99)).strftime('%Y-%m-%d')

    start_date = request.GET.get('created_after')
    end_date = request.GET.get('created_before')

    if not start_date:
        start_date = fromstart
    if not end_date:
        end_date = today

    filter_search = ReportFilter(request.GET, queryset=Report.objects.filter(
        created_at__gt=start_date,
        created_at__lte=end_date,
        is_confirmed__exact=True,
    ).order_by(sort))

    paginator = Paginator(filter_search, 30)
    page = request.GET.get('page')
    try:
        paged_reports = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paged_reports = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paged_reports = paginator.page(paginator.num_pages)

    test = "a"

    filtered_with_subs = filter_search.qs.extra(
        select={
            'sub_count': 'SELECT COUNT(*) FROM report_subscribers \
                         WHERE report_subscribers.report_id = reports.id\
                         AND report_subscribers.report_id IN %s \
                        ' % "(%s)" % ",".join([str(r.id) for r in paged_reports.object_list])

        },
        order_by=[sort]
    )

    paginator = Paginator(filtered_with_subs, 30)
    try:
        paged_reports = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paged_reports = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paged_reports = paginator.page(paginator.num_pages)

    context = {'filter': filter_search,
               'reports': paged_reports,
               'sortform': sortform
    }

    return render_to_response(template, context, context_instance=RequestContext(request))
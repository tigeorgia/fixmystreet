# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django_filters.views import FilterView
from django.views.generic.detail import DetailView

from apps.mainapp.models import Report, ReportUpdate, FixMyStreetMap
from apps.mainapp.forms import ReportUpdateForm, sortingForm
from apps.mainapp.filters import ReportFilter
from apps.mainapp.utils import random_image


class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/show.html'
    context_object_name = 'report'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ReportDetailView, self).get_context_data(**kwargs)
        context['update_form'] = ReportUpdateForm()
        context['updates'] = ReportUpdate.active.filter(report=self.object).order_by("created_at")[1:]
        context['google'] = FixMyStreetMap(self.object.point)
        return context


def poster(request, pk):
    # Build URL
    report = get_object_or_404(Report, pk=pk)
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
        return ctx

    def get_queryset(self):
        qs = self.model.active.all()
        qs = qs.extra(
            select={
                'sub_count': 'SELECT COUNT(*)\
                                FROM report_subscribers\
                                WHERE reports.id = report_subscribers.report_id'
            }
        )
        qs = qs.prefetch_related('ward', 'category')

        return qs
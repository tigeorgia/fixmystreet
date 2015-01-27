from django.shortcuts import render_to_response, get_object_or_404
from django.http import JsonResponse
from django.template import RequestContext
from django.views.generic.edit import FormView, CreateView
import json

from apps.mainapp.models import Report, ReportUpdate, FixMyStreetMap
from apps.mainapp.forms import ReportUpdateForm


class CreateReportUpdateView(CreateView):
    form_class = ReportUpdateForm
    template_name = 'reports/show.html'
    model = ReportUpdate
    object = None

    def get_form_kwargs(self):
        kwargs = super(CreateReportUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['report'] = Report.objects.get(pk=self.kwargs.get('pk'))
        return kwargs

    def form_valid(self, form):
        if self.request.is_ajax():
            report = Report.objects.get(pk=self.kwargs.get('pk'))
            self.object = form.save(commit=False)
            self.object.report = report
            self.object.report.status = form.instance.status
            self.object.user = self.request.user
            self.object.report.save()
            self.object.save()
            return JsonResponse({'success': True}, status=201)


    def form_invalid(self, form):
        if self.request.is_ajax():
            errors = {'errors': [e for e in form.errors['__all__']]}
            return JsonResponse(errors, status=400, safe=False)
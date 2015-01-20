from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views.generic.edit import FormView, CreateView

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
        return kwargs

    def form_valid(self, form):
        report = Report.objects.get(pk=self.kwargs.get('pk'))
        self.object = form.save(commit=False)
        self.object.report = report
        self.object.user = self.request.user
        self.object.save()

        return super(CreateReportUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        pass


def create(request):
    return render_to_response("reports/updates/create.html", {}, context_instance=RequestContext(request))


def confirm(request, confirm_token):
    update = get_object_or_404(ReportUpdate, confirm_token=confirm_token)

    if update.is_active:
        return HttpResponseRedirect(update.report.get_absolute_url())

    # Update main report model with status
    update.report.status = update.status
    if update.is_fixed and not update.report.is_fixed:
        update.report.fixed_at = update.created_at
    else:
        update.report.fixed_at = None

    update.is_active = True
    update.save()

    # we track a last updated time in the report to make statistics 
    # (such as on the front page) easier.  

    if not update.first_update:
        update.report.updated_at = update.created_at
    else:
        update.report.updated_at = update.report.created_at
        update.report.is_confirmed = True

    update.report.save()
    update.send_emails()

    # redirect to report    
    return HttpResponseRedirect(update.report.get_absolute_url())

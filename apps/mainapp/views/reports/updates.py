from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext

from apps.mainapp.models import Report, ReportUpdate, FixMyStreetMap
from apps.mainapp.forms import ReportUpdateForm


def new(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if request.method == 'POST':
        update_form = ReportUpdateForm(report_id=report_id, data=request.POST, files=request.FILES)
        if update_form.is_valid():
            update = update_form.save(commit=False)
            update.report = report
            update.save()
            # redirect after a POST
            return ( HttpResponseRedirect('/reports/updates/create/') )
    else:
        update_form = ReportUpdateForm()

    return render_to_response("reports/show.html",
                              {"report": report,
                               "google": FixMyStreetMap(report.point),
                               "update_form": update_form,
                              },
                              context_instance=RequestContext(request))


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

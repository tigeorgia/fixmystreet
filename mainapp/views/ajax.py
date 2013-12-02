from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import Context, RequestContext
from django.views.generic.list import ListView
from mainapp.forms import ReportStart
from mainapp.models import Report, ReportCategory, ReportCategoryClass
from django.utils.translation import ugettext as _
import json


class latestReportsJson(ListView):
    model = Report




def latest_reports_json(request):
    reports = Report.objects.all().filter(is_confirmed=True).order_by('-created_at')[:800]

    data = json.dumps([{'id': r.id,
                        'author': r.author,
                        'title': r.title,
                        'created_at': r.created_at.isoformat(),
                        'is_fixed': r.is_fixed,
                        'description': r.desc[:300] + '...',
                        'point': json.loads(r.point.json)} for r in reports], cls=DjangoJSONEncoder)
    return HttpResponse(data, 'json')


def category_desc(request, id):
    return render_to_response("ajax/category_description.html",
                {"category": ReportCategory.objects.get(id=id),
                  },
                context_instance=RequestContext(request))

def address_search_form(request):
    return render_to_response("ajax/address_geocode_form.html")

def new_report(request):
    """Pre-fill form fields from homepage"""
    preform_form = ReportStart()
    category_error = None

    if request.method == "POST":
        post_data = request.POST.copy()
        preform_form = ReportStart(data=post_data)

        request.session['_pre_form'] = post_data
        return HttpResponseRedirect("/reports/new")


    return render_to_response("ajax/new-report.html",
                              {"form": preform_form,
                               "categories": ReportCategory.objects.all().order_by("category_class"),
                               "category_error": category_error, })
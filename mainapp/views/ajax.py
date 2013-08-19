from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import Context, RequestContext
from mainapp.forms import ReportStart
from mainapp.models import ReportCategory, ReportCategoryClass
from django.utils.translation import ugettext as _

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
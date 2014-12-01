from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Count

from apps.mainapp.models import City, Report, ReportCategory, CityTotals, CityWardsTotals, AllCityTotals, \
    CityMap


def index(request):
    return render_to_response("cities/index.html",
                              {"report_counts": AllCityTotals(request.LANGUAGE_CODE)},
                              context_instance=RequestContext(request))


def show(request, city_id):
    city = get_object_or_404(City, id=city_id)
    categories = ReportCategory.objects.all().order_by("category_class")

    #top problems
    top_problems = Report.objects.filter(ward__city=city,status__exact='not-fixed').annotate(subscriber_count=Count(
        'reportsubscriber' ) ).filter(subscriber_count__gte=1).order_by('-subscriber_count')[:10]
    if request.GET.has_key('test'):
        google = CityMap(city)
    else:
        google = None

    return render_to_response("cities/show.html",
                              {"city": city,
                               "categories": categories,
                               "google": google,
                               'top_problems': top_problems,
                               "report_counts": CityWardsTotals(city, request.LANGUAGE_CODE)},
                              context_instance=RequestContext(request))


def home(request, city, error_msg, disambiguate):
    #top problems
    top_problems = Report.objects.filter(ward__city=city, is_fixed=False).annotate(
        subscriber_count=Count('reportsubscriber')).filter(subscriber_count__gte=1).order_by('-subscriber_count')[:10]
    reports_with_photos = Report.objects.filter(is_confirmed=True, ward__city=city).exclude(photo='').order_by(
        "-created_at")[:3]
    recent_reports = Report.objects.filter(is_confirmed=True, ward__city=city).order_by('-created_at')[:5]

    return render_to_response("cities/home.html",
                              {"report_counts": CityTotals('1 year', city),
                               "cities": City.objects.all(),
                               'city': city,
                               'top_problems': top_problems,
                               "reports_with_photos": reports_with_photos,
                               "recent_reports": recent_reports,
                               'error_msg': error_msg,
                               'disambiguate': disambiguate},
                              context_instance=RequestContext(request))


def category(request, city_id, category_id):
    city = get_object_or_404(City, id=city_id)
    reports = Report.objects.filter(ward__city=city, category=category_id, is_confirmed=True, is_fixed=True).order_by(
        "created_at")

    reportsuf = Report.objects.filter(ward__city=city, category=category_id, is_confirmed=True,
                                      is_fixed=False).order_by("created_at")

    return render_to_response("cities/category.html",
                              {'reports': reports,
                               'reportsuf': reportsuf,
                               'category': get_object_or_404(ReportCategory, id=category_id)},
                              context_instance=RequestContext(request))

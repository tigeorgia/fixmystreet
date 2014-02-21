from mainapp.models import FixMyStreetMap, ReportCountQuery, FaqEntry, ReportCategory, GmapPoint
from django.views.generic import TemplateView, CreateView
from mainapp.forms import ReportStart
from mainapp.utils import random_image
import datetime


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        ctx['report_counts'] = ReportCountQuery('1 year')
        ctx['center'] = GmapPoint(point=(44.79847, 41.708484))
        ctx['last_year'] = (datetime.datetime.today() + datetime.timedelta(-365)).strftime('%Y-%m-%d')
        ctx['categories'] = ReportCategory.objects.all().order_by("category_class")
        ctx['pre_form'] = ReportStart()
        ctx['google'] = FixMyStreetMap(ctx['center'], True)
        ctx['random_image'] = random_image()
        return ctx


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        ctx = super(AboutView, self).get_context_data(**kwargs)
        ctx['faq_entries'] = FaqEntry.objects.all().order_by('order')
        return ctx
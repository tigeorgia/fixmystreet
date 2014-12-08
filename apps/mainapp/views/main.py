import datetime

from django.views.generic import TemplateView

from apps.mainapp.models import Report, FixMyStreetMap, FaqEntry, ReportCategory, GmapPoint, City
from apps.mainapp.forms import ReportStart
from apps.mainapp.utils import random_image, ReportCount
from apps.users.forms import FMSUserLoginForm, FMSCheckEmailForm


class HomeView(TemplateView):
    template_name = 'home.html'
    cities = City.get_all_cities

    def _reports_with_photos(self):
        try:
            problems_with_photo = Report.active.order_by(
                '-created_at').exclude(photo__isnull=True).exclude(photo__iexact='')
        except IndexError:
            return

        photos = {
            'photos_fixed': problems_with_photo.filter(status__exact='fixed')[:10],
            'photos_not_fixed': problems_with_photo.filter(status__exact='not-fixed')[:10]
        }
        return photos

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        ctx['report_counts'] = ReportCount.by_interval('1 year')
        ctx['center'] = GmapPoint(point=(44.79847, 41.708484))
        ctx['last_year'] = (datetime.datetime.today() + datetime.timedelta(-365)).strftime('%Y-%m-%d')
        ctx['categories'] = ReportCategory.objects.all().order_by("category_class")
        ctx['check_email'] = FMSCheckEmailForm()
        ctx['ajax_login'] = FMSUserLoginForm()
        ctx['pre_form'] = ReportStart()
        ctx['google'] = FixMyStreetMap(ctx['center'], True)
        ctx['random_image'] = random_image()
        ctx['photos'] = self._reports_with_photos()
        ctx['cities'] = self.cities
        return ctx


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        ctx = super(AboutView, self).get_context_data(**kwargs)
        ctx['faq_entries'] = FaqEntry.objects.all().order_by('order')
        return ctx
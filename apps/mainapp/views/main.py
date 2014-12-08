import datetime

from django.views.generic import TemplateView
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.gis.geos import fromstr

from apps.mainapp.models import Report, FixMyStreetMap, FaqEntry, ReportCategory, GmapPoint, City
from apps.mainapp.forms import ReportForm1, ReportForm2
from apps.mainapp.utils import random_image, ReportCount
from apps.users.forms import FMSUserLoginForm, FMSCheckEmailForm
import os


class HomeView(SessionWizardView):
    form_list = [('report_start', ReportForm1), ('report_description', ReportForm2)]
    form_templates = {'report_start': 'home.html', 'report_description': 'reports/new.html'}
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))
    cities = City.get_all_cities

    def done(self, form_list, **kwargs):
        form_data = [form.cleaned_data for form in form_list]

    def get_template_names(self):
        return [self.form_templates[self.steps.current]]

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
        start_form_data = self.get_cleaned_data_for_step('report_start')
        try:
            center = (start_form_data.get('lon'), start_form_data.get('lat')) or (44.79847, 41.708484)
        except AttributeError:
            center = (44.79847, 41.708484)
        point_str = "POINT(" + str(center[0]) + " " + str(center[1]) + ")"
        pnt = fromstr(point_str, srid=4326)

        ctx = super(HomeView, self).get_context_data(**kwargs)
        ctx['report_counts'] = ReportCount.by_interval('1 year')
        ctx['center'] = GmapPoint(point=center)
        ctx['last_year'] = (datetime.datetime.today() + datetime.timedelta(-365)).strftime('%Y-%m-%d')
        ctx['categories'] = ReportCategory.objects.all().order_by("category_class")
        ctx['check_email'] = FMSCheckEmailForm()
        ctx['ajax_login'] = FMSUserLoginForm()
        ctx['google'] = FixMyStreetMap(pnt=pnt, draggable=True)
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
import datetime
import os

from django.views.generic import TemplateView
from formtools.wizard.views import SessionWizardView
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.gis.geos import fromstr
from django.contrib.auth import authenticate, login
from django.utils.translation import get_language, ugettext_lazy as _
from django.http import HttpResponseRedirect, HttpResponse

from utils.utils import get_client_ip

from apps.mainapp import models as mainapp_models
from apps.mainapp.forms import ReportForm1, ReportForm2
from apps.mainapp.utils import random_image, ReportCount
from apps.users.forms import FMSUserLoginForm, FMSCheckEmailForm, FMSUserCreationForm
from apps.users.models import FMSUser
from apps.users.forms import FMSUserCreationForm


class HomeView(SessionWizardView):
    form_list = [('report_start', ReportForm1), ('report_description', ReportForm2)]
    form_templates = {'report_start': 'home.html', 'report_description': 'reports/new.html'}
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))
    cities = mainapp_models.City.get_all_cities

    def __init__(self, **kwargs):
        super(HomeView, self).__init__(**kwargs)
        self.form_data = {}

    def _fix_data(self):
        self._merge_point()
        self._separate_data()

    def _merge_point(self):
        if 'lon' and 'lat' in self.form_data.keys():
            lon, lat = self.form_data['lon'], self.form_data['lat']
            point_str = 'POINT({0} {1})'.format(lon, lat)
            del self.form_data['lon']
            del self.form_data['lat']
            self.form_data['point'] = fromstr(point_str, srid=4326)

    def _separate_data(self):
        """
        Separate user and report data
        """
        report_fields = mainapp_models.Report._meta.get_all_field_names()
        user_fields = FMSUser._meta.get_all_field_names() + ['password1', 'password2']
        self.report_data = {field: self.form_data[field] for field in self.form_data.keys() if field in report_fields}
        self.user_data = {field: self.form_data.get(field) for field in self.form_data.keys() if field in user_fields}

    def get_report_data(self):
        return self.report_data

    def get_user_data(self):
        return self.user_data

    def get_point(self):
        return self.report_data.get('point', None)

    def _create_user(self):
        form = FMSUserCreationForm(data=self.user_data)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=self.user_data['email'],
                                password=self.user_data['password2'])
            login(self.request, user)
            return user

    def _create_report(self):
        report = mainapp_models.Report(**self.get_report_data())
        if self.request.user.is_authenticated():
            report.user = self.request.user
        else:
            report.user = self._create_user()

        report.ip = get_client_ip(self.request)
        report.ward = mainapp_models.Ward.objects.get(geom__contains=self.get_point())
        report.save()
        if report.user.is_confirmed:
            report.email_councillor()
            messages.success(self.request, _('Report was successfuly created'))
        else:
            messages.success(self.request, _('Report was successfuly created. But not yet confirmed'))
            messages.success(self.request, _('Please check your email for the confirmation link'))
        return report

    def done(self, form_list, **kwargs):
        for form in form_list:
            for field, value in form.cleaned_data.iteritems():
                if value:
                    self.form_data[field] = value
        self._fix_data()
        report = self._create_report()
        if not report:
            return HttpResponse(_('Something went crazy here. Try again. We saved your data: ') + self.report_data)
        return HttpResponseRedirect(report.get_absolute_url())

    def get_template_names(self):
        return [self.form_templates[self.steps.current]]

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step == 'report_description':
            kwargs.update({'user': self.request.user})

        return kwargs

    def _reports_with_photos(self):
        try:
            problems_with_photo = mainapp_models.Report.active.order_by(
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
        ctx['center'] = mainapp_models.GmapPoint(point=center)
        ctx['last_year'] = (datetime.datetime.today() + datetime.timedelta(-365)).strftime('%Y-%m-%d')
        ctx['categories'] = mainapp_models.ReportCategory.objects.all().order_by("name_" + get_language()[:2])
        ctx['check_email'] = FMSCheckEmailForm()
        ctx['ajax_login'] = FMSUserLoginForm()
        ctx['registration_form'] = FMSUserCreationForm
        ctx['google'] = mainapp_models.FixMyStreetMap(pnt=pnt, draggable=True)
        ctx['random_image'] = random_image()
        ctx['photos'] = self._reports_with_photos()
        ctx['cities'] = self.cities
        return ctx


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        ctx = super(AboutView, self).get_context_data(**kwargs)
        ctx['faq_entries'] = mainapp_models.FaqEntry.objects.all().order_by('order')
        return ctx
from django_filters import FilterSet, ChoiceFilter, DateTimeFilter, MethodFilter, Filter, BooleanFilter, ModelMultipleChoiceFilter
from django.utils.translation import ugettext_lazy as _
from django.forms.fields import BaseTemporalField
from django.forms.utils import from_current_timezone, to_current_timezone
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from apps.mainapp.models import City, Ward
import datetime
import pytz

from apps.mainapp.models import Report, ReportUpdate

class UnixTimeField(BaseTemporalField):
    def prepare_value(self, value):
        pass

    def to_python(self, value):
        if value:
            try:
                value = int(value)
            except ValueError:
                raise ValidationError(_('Incorrect date value'))

        if value:
            timezone = pytz.timezone(settings.TIME_ZONE)

            # Input timezone must be UTC. In order to convert
            # it to local, we must set tzinfo as utc
            date = datetime.datetime.fromtimestamp(int(value), tz=pytz.utc)

            # Convert to local time with timezone
            local_withtz = date.astimezone(timezone)
            return local_withtz
        return value

class UnixTimeFilter(Filter):
    field_class = UnixTimeField


class ReportFilter(FilterSet):
    center_point = MethodFilter(action='center_point')
    status_choices = (
        ('', '---------'),
        ('fixed', 'Fixed'),
        ('not-fixed', 'Not fixed'),
        ('in-progress', 'In progress'),
    )
    status = ChoiceFilter(choices=status_choices)
    from_date = DateTimeFilter(name='created_at', lookup_type='gte')
    to_date = DateTimeFilter(name='created_at', lookup_type='lte')
    from_date_unix = UnixTimeFilter(name='created_at', lookup_type='gte')
    to_date_unix = UnixTimeFilter(name='created_at', lookup_type='lte')
    order_by_field = 'order_by'
    city = ModelMultipleChoiceFilter(name='ward__city', queryset=City.objects.all(), widget=forms.CheckboxSelectMultiple())
    ward = ModelMultipleChoiceFilter(queryset=Ward.objects.all(), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Report
        fields = ['ward', 'city', 'category', 'from_date', 'to_date', 'from_date_unix', 'to_date_unix']
        order_by = (
            ('-created_at', _('Latest First')),
            ('created_at', _('Oldest First'))
        )

class ReportUpdateFilter(FilterSet):
    from_date = DateTimeFilter(name='created_at', lookup_type='gte')
    to_date = DateTimeFilter(name='created_at', lookup_type='lte')
    from_date_unix = UnixTimeFilter(name='created_at', lookup_type='gte')
    to_date_unix = UnixTimeFilter(name='created_at', lookup_type='lte')

    class Meta:
        model = ReportUpdate
        fields = ['user', 'report', 'status', 'from_date', 'to_date', 'from_date_unix', 'to_date_unix']
        order_by = (
            ('-created_at', _('Latest First')),
            ('created_at', _('Oldest First'))
        )


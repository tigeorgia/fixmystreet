from django_filters import FilterSet, ChoiceFilter, DateTimeFilter, MethodFilter
from django.utils.translation import ugettext_lazy as _

from apps.mainapp.models import Report


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
    order_by_field = 'order_by'

    class Meta:
        model = Report
        fields = ['ward__city', 'category', 'from_date', 'to_date']
        order_by = (
            ('-created_at', _('Latest First')),
            ('created_at', _('Oldest First'))
        )

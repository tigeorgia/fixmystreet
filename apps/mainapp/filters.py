from django_filters import FilterSet, ChoiceFilter, DateTimeFilter

from apps.mainapp.models import Report


class ReportFilter(FilterSet):
    status_choices = (
        ('', '---------'),
        ('fixed', 'Fixed'),
        ('not-fixed', 'Not fixed'),
        ('in-progress', 'In progress'),
    )
    status = ChoiceFilter(choices=status_choices)
    from_date = DateTimeFilter(name='created_at', lookup_type='gte')
    to_date = DateTimeFilter(name='created_at', lookup_type='lte')

    class Meta:
        model = Report
        fields = ['ward__city', 'category', 'from_date', 'to_date']
        order_by = True
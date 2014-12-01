from django_filters import FilterSet, ChoiceFilter

from apps.mainapp.models import Report


class ReportFilter(FilterSet):

    status_choices = (
        ('', '---------'),
        ('fixed', 'Fixed'),
        ('not-fixed', 'Not fixed'),
        ('in-progress', 'In progress'),
    )

    status = ChoiceFilter(choices=status_choices)

    class Meta:
        model = Report
        fields = ['ward__city', 'category']
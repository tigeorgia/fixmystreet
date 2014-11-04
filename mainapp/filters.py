from django_filters import FilterSet
from models import Report

class ReportFilter(FilterSet):
    class Meta:
        model = Report
        fields = ['ward__city', 'category', 'status']


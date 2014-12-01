from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from apps.api import views


urlpatterns = patterns('',
                       url(r'^login-redirect/$', views.LoginRedirectView.as_view(), name='login-redirect'),
                       url(r'^reports/$', views.ReportListCreateView.as_view(), name='reports'),
                       )

urlpatterns = format_suffix_patterns(urlpatterns)

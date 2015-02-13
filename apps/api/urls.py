from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

import views


urlpatterns = patterns('',
                       url(r'^$', views.APIRootView.as_view(), name='root'),
                       url(r'^login-redirect/$', views.LoginRedirectView.as_view(), name='login-redirect'),
                       url(r'^get-token/$', views.ObtainAuthTokenView.as_view(), name='get-token'),
                       )

urlpatterns += patterns('',
                        url(r'^reports/$', views.ReportListCreateView.as_view(), name='report-list'),
                        url(r'^reports/(?P<pk>\d+)/$', views.ReportDetailView.as_view(), name='report-detail'),
                        url(r'^reports/counts/$', views.ReportCountView.as_view(), name='report-counts'),
                        url(r'^reports/(?P<pk>\d+)/updates$', views.ReportListCreateView.as_view(),
                            name='report-updates'),
                        )

urlpatterns += patterns('',
                        url(r'^categories/$', views.CategoryListView.as_view(), name='category-list'),
                        url(r'^categories/(?P<pk>\d+)/$', views.CategoryDetailView.as_view(), name='category-detail'),
                        )

urlpatterns +=  patterns('',
                         url(r'^wards/$', views.WardListView.as_view(), name='ward-list'),
                         url(r'^wards/(?P<pk>\d+)/$', views.WardDetailView.as_view(), name='ward-detail'),
                         )

urlpatterns = format_suffix_patterns(urlpatterns)

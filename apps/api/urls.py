from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from oauth2_provider.views import AuthorizationView, TokenView
from rest_framework_social_oauth2.views import convert_token

import views

urlpatterns = [
    url(r'^auth/authorize/?$', AuthorizationView.as_view(), name="authorize"),
    url(r'^auth/token/?$', TokenView.as_view(), name="token"),
    url(r'^auth/social/$', include('social.apps.django_app.urls', namespace='social')),
    url(r'^auth/convert-token/?$', convert_token, name="convert_token"),
]

urlpatterns += [
    url(r'^$', views.APIRootView.as_view(), name='root'),
    url(r'^login-redirect/$', views.LoginRedirectView.as_view(), name='login-redirect'),
    url(r'^get-token/$', views.ObtainAuthTokenView.as_view(), name='get-token'),
    url(r'^user/$', views.ExtendedUserDetailView.as_view(), name='get-user'),
]

urlpatterns += [
    url(r'^reports/$', views.ReportListCreateView.as_view(), name='report-list'),
    url(r'^reports/(?P<pk>\d+)/$', views.ReportDetailView.as_view(), name='report-detail'),
    url(r'^reports/counts/$', views.ReportCountView.as_view(), name='report-counts'),
    url(r'^reports/(?P<pk>\d+)/updates$', views.ReportListCreateView.as_view(),
        name='report-updates'),
]

urlpatterns += [
    url(r'^categories/$', views.CategoryListView.as_view(), name='category-list'),
    url(r'^categories/(?P<pk>\d+)/$', views.CategoryDetailView.as_view(), name='category-detail'),
]

urlpatterns += [
    url(r'^wards/$', views.WardListView.as_view(), name='ward-list'),
    url(r'^wards/(?P<pk>\d+)/$', views.WardDetailView.as_view(), name='ward-detail'),
]

urlpatterns += [
    url(r'^faq/$', views.FaqEntryListView.as_view(), name='faq-list'),
]

urlpatterns += [
    url(r'^contact/$', views.ContactView.as_view(), name='contact'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

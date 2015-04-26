from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps import FlatPageSitemap
from django.views.decorators.cache import cache_page

from apps.mainapp import feeds
from apps.mainapp import sitemaps
from apps.mainapp.views import main as main_views
from apps.mainapp.views import wards as wards_views
from apps.mainapp.views import promotion as promo_views
from apps.mainapp.views import contact as contact_views
from apps.mainapp.views import ajax as ajax_views

from apps.mainapp.views.reports import main as report_views
from apps.mainapp.views.reports import updates as update_views
from apps.mainapp.views.reports import subscribers as sub_views
from apps.mainapp.views.reports import flags as flag_views


js_info_dict = {
    'packages': ('django-fixmystreet',),
}

feeds = {
    'reports': feeds.LatestReports,
    'wards': feeds.LatestReportsByWard,
    'cities': feeds.LatestReportsByCity,
    'report_updates': feeds.LatestUpdatesByReport,
}

sitemaps = {
    "main": sitemaps.MainSitemap,
    "flatpages": FlatPageSitemap
}

admin.autodiscover()

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
]

urlpatterns += i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/rosetta/', include('rosetta.urls')),
)

urlpatterns += [
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})
]

urlpatterns += i18n_patterns(
    url(r'^$', main_views.HomeView.as_view(), name='home'),
    url(r'about/$', cache_page(60 * 60 * 24)(main_views.AboutView.as_view()), name='about')
)

urlpatterns += i18n_patterns(
    url(r'^promotions/(\w+)/$', promo_views.show, name='promotions'),
)

urlpatterns += i18n_patterns(
    url(r'^wards/(?P<ward_id>\d+)/$', wards_views.show, name='ward_detail'),
    url(r'^cities/(?P<city_id>\d+)/wards/(?P<ward_id>\d+)/$', wards_views.show_by_number, name='city_ward_detail'),
)

urlpatterns += i18n_patterns(
    url(r'^reports/(?P<pk>\d+)/updates/$', update_views.CreateReportUpdateView.as_view(), name='create-report-update'),
)

urlpatterns += i18n_patterns(
    url(r'^reports/subscribers/confirm/(\S+)/$', sub_views.confirm, name='subscriber_confirm'),
    url(r'^reports/subscribers/unsubscribe/(\S+)/$', sub_views.unsubscribe, name='subscriber_unsubscribe'),
    url(r'^reports/subscribers/create/$', sub_views.create, name='subscriber_create'),
    url(r'^reports/(?P<report_id>\d+)/subscribers/$', sub_views.new, name='subscriber_new'),
)

urlpatterns += i18n_patterns(
    url(r'^reports/(?P<report_id>\d+)/flags/thanks/$', flag_views.thanks, name='flag_thanks'),
    url(r'^reports/(?P<report_id>\d+)/flags/$', flag_views.new, name='flag_new'),
)

urlpatterns += i18n_patterns(
    url(r'^reports/(?P<pk>\d+)/$', report_views.ReportDetailView.as_view(), name='report_detail'),
    url(r'^reports/(?P<pk>\d+)/poster/$', report_views.poster, name='poster'),
    url(r'^reports/$', cache_page(60 * 5)(report_views.ReportListView.as_view()), name='report_list'),
)

urlpatterns += i18n_patterns(
    url(r'^contact/thanks/$', contact_views.thanks, name='contact_thanks'),
    url(r'^contact/$', contact_views.new, name='contact_new'),
)

urlpatterns += i18n_patterns(
    url(r'^ajax/categories/(?P<cat_id>\d+)/$', ajax_views.category_desc, name='ajax_category_desc'),
    url(r'^ajax/address-search-form/$', ajax_views.address_search_form, name='ajax_address_search'),
    url(r'^ajax/latest-reports/$', ajax_views.latest_reports_json, name='ajax_latest_reports'),
    url(r'^ajax/l$', ajax_views.latestReportsJson.as_view(), name='ajax_latest_reports_json')
)

urlpatterns += i18n_patterns(
    url(r'^user/', include('apps.users.urls', namespace='users', app_name='users')),
)

urlpatterns += i18n_patterns(
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('apps.api.urls', namespace='api')),
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
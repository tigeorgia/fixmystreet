from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps import FlatPageSitemap

from mainapp.feeds import LatestReports, LatestReportsByCity, LatestReportsByWard, LatestUpdatesByReport
from mainapp.sitemaps import MainSitemap
from mainapp.views.main import AboutView, HomeView
from mainapp.views.reports.main import show as ReportShow
from mainapp.views.ajax import latestReportsJson
from mainapp.views.reports.main import ReportListView


js_info_dict = {
    'packages': ('django-fixmystreet',),
}

feeds = {
    'reports': LatestReports,
    'wards': LatestReportsByWard,
    'cities': LatestReportsByCity,
    'report_updates': LatestUpdatesByReport,
}

sitemaps = {
    "main": MainSitemap,
    "flatpages": FlatPageSitemap
}

admin.autodiscover()
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.Feed', {'feed_dict': feeds}),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

urlpatterns += patterns('django.views.i18n',
    url(r'^jsi18n/$', 'javascript_catalog', js_info_dict),
)

urlpatterns += patterns('django.contrib.sitemaps.views',
    url(r'^sitemap\.xml$', 'sitemap', {'sitemaps': sitemaps})
)

urlpatterns += i18n_patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'about/$', AboutView.as_view(), name='about')
)

urlpatterns += i18n_patterns('mainapp.views.promotion',
    url(r'^promotions/(\w+)/$', 'show', name='promotions'),
)

urlpatterns += i18n_patterns('mainapp.views.wards',
    url(r'^wards/(?P<ward_id>\d+)/$', 'show', name='ward_detail'),
    url(r'^cities/(?P<city_id>\d+)/wards/(?P<ward_id>\d+)/$', 'show_by_number', name='city_ward_detail'),

)

urlpatterns += i18n_patterns('mainapp.views.reports.updates',
    url(r'^reports/updates/confirm/(\S+)/$', 'confirm', name='report_update_confirm'),
    url(r'^reports/updates/create/$', 'create', name='report_update_create'),
    url(r'^reports/(?P<report_id>\d+)/updates/$', 'new', name='report_update_new'),
)

urlpatterns += i18n_patterns('mainapp.views.reports.subscribers',
    url(r'^reports/subscribers/confirm/(\S+)/$', 'confirm', name='subscriber_confirm'),
    url(r'^reports/subscribers/unsubscribe/(\S+)/$', 'unsubscribe', name='subscriber_unsubscribe'),
    url(r'^reports/subscribers/create/$', 'create', name='subscriber_create'),
    url(r'^reports/(?P<report_id>\d+)/subscribers/$', 'new', name='subscriber_new'),
)

urlpatterns += i18n_patterns('mainapp.views.reports.flags',
    url(r'^reports/(?P<report_id>\d+)/flags/thanks/$', 'thanks', name='flag_thanks'),
    url(r'^reports/(?P<report_id>\d+)/flags/$', 'new', name='flag_new' ),
)

urlpatterns += i18n_patterns('mainapp.views.reports.main',
    url(r'^reports/(?P<report_id>\d+)/$', ReportShow, name='report_show'),
    url(r'^reports/(?P<report_id>\d+)/poster/$', 'poster', name='poster'),
    # (r'^reports/category/(\d+)$', 'category'),
    url(r'^reports/new/$', 'new', name='report_new'),
    url(r'^reports/$', ReportListView.as_view(), name='report_list'),
)

urlpatterns += i18n_patterns('mainapp.views.contact',
    url(r'^contact/thanks/$', 'thanks', name='contact_thanks'),
    url(r'^contact/$', 'new', name='contact_new'),
)

urlpatterns += i18n_patterns('mainapp.views.ajax',
    url(r'^ajax/categories/(?P<cat_id>\d+)/$', 'category_desc', name='ajax_category_desc'),
    url(r'^ajax/address-search-form/$', 'address_search_form', name='ajax_address_search'),
    url(r'^ajax/new-report/$', 'new_report', name='ajax_report_new'),
    url(r'^ajax/latest-reports/$', 'latest_reports_json', name='ajax_latest_reports'),
    url(r'^ajax/l$', latestReportsJson.as_view(), name='ajax_latest_reports_json')
)


urlpatterns += patterns('',
                        url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
                        url(r'^api/', include('api.urls', namespace='api')),
                        )

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.contrib.staticfiles.views.serve'),
    )

    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
        )

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
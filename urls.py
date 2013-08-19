from django.conf.urls import *
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import admin
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from mainapp.feeds import LatestReports, LatestReportsByCity, LatestReportsByWard, LatestUpdatesByReport
from mainapp.models import City, Report, ReportFilter
from mainapp.sitemaps import MainSitemap
import mainapp.views.cities as cities

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

urlpatterns += patterns('',
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
)


urlpatterns += i18n_patterns('',
                        url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})
)

urlpatterns += i18n_patterns('mainapp.views.main',
                        url(r'^$', 'home'),
                        url(r'about/$', 'about')
)

urlpatterns += i18n_patterns('mainapp.views.faq',
                        url(r'^about/(\S+)$', 'show'),
)

urlpatterns += i18n_patterns('mainapp.views.promotion',
                        url(r'^promotions/(\w+)$', 'show'),
)

urlpatterns += i18n_patterns('mainapp.views.wards',
                        url(r'^wards/(?P<ward_id>\d+)', 'show'),
                        url(r'^cities/(?P<city_id>\d+)/wards/(?P<ward_id>\d+)', 'show_by_number'),

)


urlpatterns += i18n_patterns('mainapp.views.reports.updates',
                        (r'^reports/updates/confirm/(\S+)', 'confirm'),
                        (r'^reports/updates/create/', 'create'),
                        (r'^reports/(?P<report_id>\d+)/updates/', 'new'),
)

urlpatterns += i18n_patterns('mainapp.views.reports.subscribers',
                        (r'^reports/subscribers/confirm/(\S+)', 'confirm'),
                        (r'^reports/subscribers/unsubscribe/(\S+)', 'unsubscribe'),
                        (r'^reports/subscribers/create/', 'create'),
                        (r'^reports/(?P<report_id>\d+)/subscribers', 'new'),
)

urlpatterns += i18n_patterns('mainapp.views.reports.flags',
                        (r'^reports/(?P<report_id>\d+)/flags/thanks', 'thanks'),
                        (r'^reports/(?P<report_id>\d+)/flags', 'new'),
)

urlpatterns += i18n_patterns('mainapp.views.reports.main',
                        (r'^reports/(?P<report_id>\d+)$', 'show'),
                        (r'^reports/(?P<report_id>\d+)/$', 'show'),
                        (r'^reports/(?P<report_id>\d+)/poster$', 'poster'),
                        #(r'^reports/category/(\d+)$', 'category'),
                        (r'^reports/', 'new'),
)

urlpatterns += i18n_patterns('mainapp.views.contact',
                        (r'^contact/thanks', 'thanks'),
                        (r'^contact', 'new'),
)

urlpatterns += i18n_patterns('mainapp.views.ajax',
                        (r'^ajax/categories/(?P<cat_id>\d+)', 'category_desc'),
                        (r'^ajax/address-search-form', 'address_search_form'),
                        (r'^ajax/new-report$', 'new_report'),
)

urlpatterns += i18n_patterns('mainapp.views.reports',
                             (r'^all-reports/', 'main.report_list'),
)

#The following is used to serve up local media files like images
if settings.LOCAL_DEV:
    baseurlregex = r'^media/(?P<path>.*)$'
    urlpatterns += patterns('',
                            (baseurlregex, 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT}),
    )

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )
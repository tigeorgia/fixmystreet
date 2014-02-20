# coding=utf-8

import os
import logging

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
TEST_RUNNER = 'django.contrib.gis.tests.run_tests'
POSTGIS_TEMPLATE = 'template_postgis'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Tbilisi'
APPEND_SLASH = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ka'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# URL that handles the media and static served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
# Serve with nginx
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

RANDOM_IMAGE_DIR = 'images/header-images/' #random home images


#GOOGLE MAPS SETTINGS
GOOGLE_MAPS_URL = 'https://maps.googleapis.com/maps/api/js?sensor=true&v=%s&key='
GOOGLE_MAPS_API_VERSION = 3


# START Pipeline settings
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)


PIPELINE_CSS = {
    'main_css': {
        'source_filenames': (
            'custom.less',
            'css/datepicker.css',
        ),
        'output_filename': 'css.min/style.min.css',
    },

    'ie_deprecated': {
        'source_filenames': (
        ),
        'output_filename': 'css.min/ie-deprecated.min.css',
    },

    'ie': {
        'source_filenames': (
        ),
        'output_filename': 'css.min/ie.min.css',
    },
}

PIPELINE_JS = {
    'main_js': {
        'source_filenames': (
            'js/jquery.min.js',
            'js/jquery-ui.min.js',
            'js/jquery.easing.min.js',
            'js/jquery.validate.min.js',
            'bootstrap/dist/js/bootstrap.min.js',
            'js/bootstrap-datepicker.js',
            'js/jquery.qtip.min.js',
            'js/geokbd.js',
            'js/fms.js',
        ),
        'output_filename': 'js.min/scripts.min.js',
    },

    'ie_js': {
        'source_filenames': (
            'js/html5shiv.js',
            'js/respond.js',
        ),
        'output_filename': 'js.min/ie-scripts.min.js',
    },
}

PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'

PIPELINE_YUI_CSS_ARGUMENTS = ''
PIPELINE_YUI_JS_ARGUMENTS = ''

PIPELINE_ENABLED = False
# END Pipeline settings

#PREPEND_WWW = True

ADMIN_MEDIA_ROOT = 'django.contrib.admin.media'
# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# ensure large uploaded files end up with correct permissions.  See
# http://docs.djangoproject.com/en/dev/ref/settings/#file-upload-permissions

FILE_UPLOAD_PERMISSIONS = 0644
DATE_FORMAT = "l, F jS, Y"


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'mainapp.middleware.language.LanguagePrefixMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'ignore_lang.middleware.ForceDefaultLanguageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'mainapp.middleware.subdomains.SubdomainMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

LANGUAGES = (
    ('en', 'English'),
    ('ka', 'Georgian'),
)

LOCALE_PATHS = (
    os.path.join(PROJECT_PATH, 'locale'),
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.gis',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'google_analytics',
    'transmeta',
    'ignore_lang',
    'mainapp',
    'south',
    'pipeline',
    'django_filters',
    'rosetta',
    'widget_tweaks',
)

DEBUG = True
LOCAL_DEV = False

try:
    from local_settings import *
except ImportError:
    try:
        from mod_python import apache

        apache.log_error("local_settings.py not set; using default settings", apache.APLOG_NOTICE)
    except ImportError:
        import sys

        sys.stderr.write("local_settings.py not set; using default settings\n")

MANAGERS = ADMINS

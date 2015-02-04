# coding=utf-8

import os
import logging

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
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

RANDOM_IMAGE_DIR = 'images/header-images/'  # random home images
LOGIN_REDIRECT_URL = 'api:login-redirect'

# GOOGLE MAPS SETTINGS
GOOGLE_MAPS_URL = 'https://maps.googleapis.com/maps/api/js?sensor=true&v=%s&key='
GOOGLE_MAPS_API_VERSION = 3

DEBUG_TOOLBAR_PATCH_SETTINGS = False

# START Pipeline settings
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

#If javascript breaks, set this to true
PIPELINE_DISABLE_WRAPPER = True

PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)

PIPELINE_CSS = {
    'main_css': {
        'source_filenames': (
            'app.less',
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
            'js/jquery.lazyload.min.js',
            'js/jquery.cookie.js',
            'js/OpenLayers.js',
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

PIPELINE_ENABLED = True
# END Pipeline settings

#PREPEND_WWW = True

ADMIN_MEDIA_ROOT = 'django.contrib.admin.media'
ADMIN_MEDIA_PREFIX = '/static/admin/'

FILE_UPLOAD_PERMISSIONS = 0644
DATE_FORMAT = "l, F jS, Y"

AUTH_USER_MODEL = 'users.FMSUser'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'ignore_lang.middleware.ForceDefaultLanguageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'apps.mainapp.middleware.subdomains.SubdomainMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',
                                'rest_framework.filters.OrderingFilter'),
    'PAGINATE_BY': 30,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 100,
    'ORDERING_PARAM': 'order_by',
    'DEFAULT_MODEL_SERIALIZER_CLASS': 'rest_framework.serializers.ModelSerializer'
}

LANGUAGES = (
    ('en', 'English'),
    ('ka', 'Georgian'),
)

LOCALE_PATHS = (
    os.path.join(PROJECT_PATH, 'locale'),
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
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
    'django.contrib.formtools',
    'transmeta',
    'ignore_lang',
    'apps.mainapp',
    'apps.api',
    'apps.users',
    'pipeline',
    'django_filters',
    'debug_toolbar',
    'rosetta',
    'widget_tweaks',
    'rest_framework',
    'rest_framework.authtoken',
    'stdimage',
    'bootstrap3',
    'captcha',
    'crispy_forms'
)

DEBUG = False
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


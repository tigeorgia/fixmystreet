# coding=utf-8

import os
import logging


######################################
# ############ VARIABLES #############
######################################

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
TEST_RUNNER = 'django.contrib.gis.tests.run_tests'
POSTGIS_TEMPLATE = 'template_postgis'

######################################


######################################
# ############# LOCALE ###############
######################################

TIME_ZONE = 'Asia/Tbilisi'
LANGUAGE_CODE = 'ka'
USE_I18N = True
DATE_FORMAT = "l, F jS, Y"
LANGUAGES = (
    ('en', 'English'),
    ('ka', 'Georgian'),
)

LOCALE_PATHS = (
    os.path.join(PROJECT_PATH, 'locale'),
)

######################################


######################################
# ############ URL & PATH ############
######################################

APPEND_SLASH = True
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
RANDOM_IMAGE_DIR = 'images/header-images/'
LOGIN_REDIRECT_URL = 'api:login-redirect'
# PREPEND_WWW = True
ADMIN_MEDIA_ROOT = 'django.contrib.admin.media'
ADMIN_MEDIA_PREFIX = '/static/admin/'

######################################


######################################
# ############ GOOGLE MAPS ###########
######################################

GOOGLE_MAPS_URL = 'https://maps.googleapis.com/maps/api/js?sensor=true&v=%s&key='
GOOGLE_MAPS_API_VERSION = 3

######################################


######################################
# ############ STATICFILES ###########
######################################

FILE_UPLOAD_PERMISSIONS = 0644

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
# If javascript breaks, set this to true
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
    'jquery': {
        'source_filenames': (
            'js/jquery.min.js',
            'js/jquery-ui.min.js',
            'js/jquery.easing.min.js',
            'js/jquery.validate.min.js',
            'js/jquery.lazyload.min.js',
            'js/jquery.cookie.js',
        ),
        'output_filename': 'js.min/jquery.min.js'
    },
    'lib': {
        'source_filenames': (
            'js/markerclusterer_compiled.js',
            'js/OpenLayers.js',
            'bootstrap/dist/js/bootstrap.min.js',
            'js/bootstrap-datepicker.js',
            'js/jquery.qtip.min.js',
            'js/geokbd.js',
        ),
        'output_filename': 'js.min/lib.min.js',
    },

    'app': {
        'source_filenames': (
            'js/fms.js',
            'js/fms.forms.js',
            'js/fms.map.js',
        ),
        'output_filename': 'js.min/app.min.js',
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

######################################


######################################
# ############# TEMPLATE #############
######################################

CRISPY_TEMPLATE_PACK = 'bootstrap3'

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
    "django.contrib.messages.context_processors.messages",
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
)

######################################


######################################
# ############ MIDDLEWARE ############
######################################

MIDDLEWARE_CLASSES = (
    'apps.mainapp.middleware.webfaction.WebFactionFixes',
    'apps.mainapp.middleware.staging.RestrictStagingAccess',
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

######################################


######################################
# ########## REST FRAMEWORK ##########
######################################

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

######################################


######################################
# ############## AUTH ################
######################################

AUTH_USER_MODEL = 'users.FMSUser'

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)

######################################


######################################
# ############## APPS ################
######################################

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
    'formtools',
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
    'stdimage',
    'bootstrap3',
    'captcha',
    'crispy_forms',
)

######################################


######################################
# ############ VARIOUS ###############
######################################

DEBUG_TOOLBAR_PATCH_SETTINGS = False

######################################


######################################
# ############ LOGGING ###############
######################################

LOG_PATH = os.path.join(PROJECT_PATH, 'var/log/')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'apps.mainapp.deferred_logging.DefferedFileHandler',
            'filename': 'error.log',
        },
        'mail_admins': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'mail_admins']
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'stdimage': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'fms': {
            'handlers': ['file', 'mail_admins'],
            'level': 'WARNING',
            'propagate': True,
        }
    },
}

######################################


from local_settings import *

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = os.path.join(PROJECT_PATH, 'var/log/email.log')
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': os.path.join(PROJECT_PATH, 'var/cache/'),
            'TIMEOUT': 300
        }
    }

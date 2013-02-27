# Django settings for fixmystreet project.
# This is a change that we want to keep
import os
import logging

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
TEST_RUNNER='django.contrib.gis.tests.run_tests'
POSTGIS_TEMPLATE = 'template_postgis'

# Turning off logging for the moment. -DD
#logging.basicConfig(
#    level = logging.DEBUG,
#    format = '%(asctime)s %(levelname)s %(message)s',
#    filename = '/tmp/fixmystreet.log',
#    filemode = 'w'
#)
        
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Tbilisi'
APPEND_SLASH=True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ka'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/path/to/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'


ADMIN_MEDIA_ROOT = 'django.contrib.admin.media'
# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# ensure large uploaded files end up with correct permissions.  See
# http://docs.djangoproject.com/en/dev/ref/settings/#file-upload-permissions

FILE_UPLOAD_PERMISSIONS = 0644
DATE_FORMAT = "l, F jS, Y"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'ignore_lang.middleware.ForceDefaultLanguageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'mainapp.middleware.subdomains.SubdomainMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)


LANGUAGES = (
  ('en','English'),
  ('ka', 'Georgian'),
)


ROOT_URLCONF = 'fixmystreet.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.gis',
    'django.contrib.flatpages',
    'google_analytics', # used to be 'contrib.google_analytics',
    'contrib.transmeta',
    'ignore_lang',
    'mainapp',
    'south',
)


#################################################################################
# These variables Should be defined in the local settings file
#################################################################################
#
#DATABASE_ENGINE =            # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#DATABASE_NAME =              # Or path to database file if using sqlite3.
#DATABASE_USER =              # Not used with sqlite3.
#DATABASE_PASSWORD =          # Not used with sqlite3.
#DATABASE_HOST = ''  nge the types of two existing colu           # Set to empty string for localhost. Not used with sqlite3.
#DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
#
#EMAIL_USE_TLS =
#EMAIL_HOST =
#EMAIL_HOST_USER =
#EMAIL_HOST_PASSWORD =
#EMAIL_PORT =
#EMAIL_FROM_USER =
DEBUG = True
#LOCAL_DEV =
#SITE_URL = http://localhost:8000
#SECRET_KEY=
#GMAP_KEY=
#
#ADMIN_EMAIL = 
#ADMINS =
#####################################################################################

# import local settings overriding the defaults
# local_settings.py is machine independent and should not be checked in

try:
    from local_settings import *
except ImportError:
    try:
        from mod_python import apache
        apache.log_error( "local_settings.py not set; using default settings", apache.APLOG_NOTICE )
    except ImportError:
        import sys
        sys.stderr.write( "local_settings.py not set; using default settings\n" )


MANAGERS = ADMINS

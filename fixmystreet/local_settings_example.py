DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '',
        'USER': '',
        'PASSWORD': ''
    }
}

INTERNAL_IPS = ['127.0.0.1']

ALLOWED_HOSTS = ['localhost']

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
# Serve with nginx
MEDIA_ROOT = ""

# Absolute path to the directory that holds static.
# Example: "/home/static/static.lawrence.com/"
# Serve with nginx
STATIC_ROOT = ""

# Path to less compiler binary
PIPELINE_LESS_BINARY = (
    '/usr/local/bin/lessc'
)
ROOT_URLCONF = 'fixmystreet.urls'

# Path to YUI binary
PIPELINE_YUI_BINARY = '/bin/yuicompressor'

EMAIL_USE_TLS = ''
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = '25'
EMAIL_FROM_USER = 'system@mysite.com'
SERVER_EMAIL = EMAIL_FROM_USER
DEBUG = True
PIPELINE_ENABLED = not DEBUG
LOCAL_DEV = 'http://127.0.0.1:8000'
SITE_URL = 'http://mysite.com'
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
PREPEND_WWW = False

# Google maps API key. Learn how to obtain here:
# https://developers.google.com/maps/documentation/javascript/tutorial#api_key
GMAP_KEY = ''
GOOGLE_MAPS_API_VERSION = '2.0'
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
RECAPTCHA_USE_SSL = True

# Set this or Django won't run
SECRET_KEY = ''

SITE_ID = 0
ADMIN_EMAIL = 'chemikucha@mysite.com'
ADMINS = (('Name', 'admin@mysite.com'),)


if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/var/tmp/chemikucha_cache',
            'TIMEOUT': 300
        }
    }

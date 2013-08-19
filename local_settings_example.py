DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '',
        'USER': '',
        'PASSWORD': ''
    }
}

ALLOWED_HOSTS = ['mysite.com', 'www.mysite.com']
EMAIL_USE_TLS = ''
EMAIL_HOST = 'smtp.mysite.com'
EMAIL_HOST_USER = 'chemikucha'
EMAIL_HOST_PASSWORD = 'chemikucha'
EMAIL_PORT = '25'
EMAIL_FROM_USER = 'system@mysite.com'
DEBUG = True 
LOCAL_DEV = 'http://127.0.0.1:8000'
SITE_URL = 'http://mysite.com'
# Google maps API key. Learn how to obtain here:
# https://developers.google.com/maps/documentation/javascript/tutorial#api_key
GMAP_KEY = ''
GOOGLE_MAPS_API_VERSION = '2.0'
# Set this or Django won't run
SECRET_KEY = ''
SITE_ID= 0
ADMIN_EMAIL = 'chemikucha@mysite.com'
ADMINS = ['Chemi Kucha']
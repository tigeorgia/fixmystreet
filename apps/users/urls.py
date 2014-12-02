from django.conf.urls import patterns, url
from .views import EmailExistsView

urlpatterns = patterns('',
                       url(r'^email-exists$', EmailExistsView.as_view()),
)
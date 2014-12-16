from django.conf.urls import patterns, url
import views
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
                       url(r'^email-exists$', views.EmailExistsView.as_view()),
                       url(r'^ajax/login/$', views.AjaxLoginView.as_view()),
                       url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout')
)
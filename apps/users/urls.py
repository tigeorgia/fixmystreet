from django.conf.urls import patterns, url
import views
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
                       url(r'^email-exists$', views.EmailExistsView.as_view()),
                       url(r'^confirm/(?P<token>\w+)/$', views.TokenConfirmationView.as_view(), name='confirm'),
                       url(r'^login/$', views.LoginView.as_view(), name='login'),
                       url(r'^ajax/login/$', views.AjaxLoginView.as_view(), name='ajaxlogin'),
                       url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout')
)
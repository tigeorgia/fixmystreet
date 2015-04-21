from django.conf.urls import patterns, url
import views
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
                       url(r'^register/$', views.RegistrationView.as_view()),
                       url(r'^confirm/(?P<token>\w+)/$', views.TokenConfirmationView.as_view(), name='confirm'),
                       url(r'^login/$', views.LoginView.as_view(), name='login'),
                       url(r'^reset/$', views.PasswordResetView.as_view(), name='reset'),
                       url(r'^reset/(?P<token>\w+)/$', views.PasswordResetConfirmView.as_view(), name='reset_confirm'),
                       url(r'^ajax/login/$', views.AjaxLoginView.as_view(), name='ajaxlogin'),
                       url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout')
)
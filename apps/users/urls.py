from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^email-exists$', views.EmailExistsView.as_view()),
                       url(r'^ajax/login/$', views.AjaxLoginView.as_view()),
)
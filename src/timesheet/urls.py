from django.conf.urls import include, url

from timesheet import views


urlpatterns = [
    url(r'^testform/', views.test_form, name='test_form'),
    url(r'^formdesign/', views.form_design, name='form_design'),
    url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', views.index, name='index'),
    url(r'^', views.index, name='index'),

]
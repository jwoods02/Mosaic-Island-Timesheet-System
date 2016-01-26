from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', views.month_view, name='month_view'),
    url(r'^options/$', views.options, name='options'),
    url(r'^summary/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', views.summary_month, name='summary_month'),
    url(r'^summary/departments/$', views.summary_departments, name='summary_departments'),
    url(r'^summary/activities/$', views.summary_activities, name='summary_activities'),
    url(r'^summary/(?P<employee>[0-9]+)/$', views.summary_employees, name='summary_employees'),

]
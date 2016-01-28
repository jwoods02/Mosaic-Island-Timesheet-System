from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', views.month_view, name='month_view'),
    url(r'^options/$', views.options, name='options'),
    url(r'^summary/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', views.summary_month, name='summary_month'),
]
#!usr/bin/env python
#coding: utf-8
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
     #url(r'^$', 'showchart.views.getchart',name="showchart"),
     url(r'^getChartId/$', 'showchart.views.getChartId', name="showchart_getChartId"),
     url(r'^getChartInfo/$', 'showchart.views.getChartInfo', name="showchart_getChartInfo"),
     
)
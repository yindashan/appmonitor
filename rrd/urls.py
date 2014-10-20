#!usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
     url(r'^$', 'rrd.views.chartdata',name="rrd"),
     url(r'^chartdata/$', 'rrd.views.chartdata', name="rrd_chartdata"),
     url(r'^precisedata/$', 'rrd.views.precisedata', name="rrd_precisedata"),
)

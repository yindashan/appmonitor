#!usr/bin/env python
#coding: utf-8
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
     url(r'^$', 'checkresult.views.index',name="checkresult"),
     url(r'^index/$', 'checkresult.views.index', name="checkresult_index"),
     url(r'^taskdetail/(?P<task_id>\d+)/$', 'checkresult.views.taskdetail', name="checkresult_taskdetail"),
     url(r'^watch/(?P<result_id>\d+)/$', 'checkresult.views.watch', name="checkresult_watch"),
)
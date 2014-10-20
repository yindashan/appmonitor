#!usr/bin/env python
#coding: utf-8
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',

     url(r'^$', 'appitem.views.index',name="appitem"),
     url(r'^index/$', 'appitem.views.index', name="appitem_index"),
     url(r'^add/$', 'appitem.views.add', name="appitem_add"),
     url(r'^edit/(?P<app_id>\d+)/$', 'appitem.views.edit',name="appitem_edit"),
     url(r'^delete/(?P<app_id>\d+)/$', 'appitem.views.delete',name="appitem_delete"),
#     url(r'^search/$', 'appitem.views.search',name="appitem_search"),
     url(r'^selecteddelete/$', 'appitem.views.selecteddel',name="appitem_selecteddelete"),
     url(r'^getappinfo/$', 'appitem.views.getappinfo',name="appitem_getappinfo"),
     url(r'^getcombine/$', 'appitem.views.getAppCombineChart',name="appitem_getcombine"),
)
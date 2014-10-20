#!usr/bin/env python
#coding: utf-8
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
     url(r'^$', 'servicegroup.views.index',name="servicegroup"),
     url(r'^index/$', 'servicegroup.views.index', name="servicegroup_index"),
     url(r'^add/$', 'servicegroup.views.add', name="servicegroup_add"),
     url(r'^edit/(?P<group_id>\d+)/$', 'servicegroup.views.edit',name="servicegroup_edit"),
     url(r'^delete/(?P<group_id>\d+)/$', 'servicegroup.views.delete',name="servicegroup_delete"),
     url(r'^selecteddelete/$', 'servicegroup.views.selecteddel',name="servicegroup_selecteddelete"),
)
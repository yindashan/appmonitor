#!usr/bin/env python
#coding: utf-8
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
     url(r'^$', 'caseset.views.index',name="caseset"),
     url(r'^index/$', 'caseset.views.index', name="caseset_index"),
     url(r'^add/$', 'caseset.views.add', name="caseset_add"),
     url(r'^edit/(?P<set_id>\d+)/$', 'caseset.views.edit',name="caseset_edit"),
     url(r'^delete/(?P<set_id>\d+)/$', 'caseset.views.delete',name="caseset_delete"),
     url(r'^selecteddelete/$', 'caseset.views.selecteddel',name="caseset_selecteddelete"),
     url(r'^execute/(?P<set_id>\d+)/$', 'caseset.views.execute',name="caseset_execute"),
     url(r'^execute/(?P<set_id>\d+)/$', 'caseset.views.execute',name="caseset_execute"),
)
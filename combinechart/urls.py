#!usr/bin/env python
#coding: utf-8
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
     url(r'^$', 'combinechart.views.index',name="combinechart"),
     url(r'^index/$', 'combinechart.views.index',name="combinechart_index"),
     url(r'^add/$', 'combinechart.views.add',name="combinechart_add"),
     url(r'^edit/(?P<item_id>\d+)/$', 'combinechart.views.edit', name="combinechart_edit"),
     url(r'^delete/(?P<item_id>\d+)/$', 'combinechart.views.delete', name="combinechart_delete"),
     url(r'^selecteddelete/$', 'combinechart.views.selecteddel',name="combinechart_selecteddelete"),
     url(r'^getcombinechart/$', 'combinechart.views.getCombineChart',name="combinechart_getcombinechart"),
     url(r'^search/$', 'combinechart.views.search',name="combinechart_search"),
)
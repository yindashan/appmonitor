#!usr/bin/env python
#coding: utf-8
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
     url(r'^$', 'product.views.index',name="product"),
     url(r'^index/$', 'product.views.index', name="product_index"),
     url(r'^add/$', 'product.views.add', name="product_add"),
     url(r'^edit/(?P<product_id>\d+)/$', 'product.views.edit',name="product_edit"),
     url(r'^delete/(?P<product_id>\d+)/$', 'product.views.delete',name="product_delete"),
     url(r'^selecteddelete/$', 'product.views.selecteddel',name="product_selecteddelete"),
)
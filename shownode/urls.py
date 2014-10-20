# -*- coding:utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
     url(r'^$', 'shownode.views.tree',name="shownode"),
     url(r'^tree/$', 'shownode.views.tree', name="shownode_tree"),
     # 用于配置节点读写权限
     url(r'^righttree/$', 'shownode.views.righttree', name="shownode_righttree"),
     url(r'^manipulate_tree/$', 'shownode.views.manipulate_tree', name="shownode_manipulate_tree"),
     url(r'^getCurrRelation/$', 'shownode.views.getCurrRelation', name="shownode_getCurrRelation"),
     url(r'^getchart/$', 'shownode.views.getchart', name="shownode_getchart"),
     # 业务视图
     url(r'^businessview/$', 'shownode.views.businessview', name="shownode_businessview"),
)
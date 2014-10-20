#!usr/bin/env python
# -*- coding:utf-8 -*-
#django
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import *
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required

# standard library
import json

#our own code
from showchart.models import Chart,ChartExtend
from monitoritem.models import MonitorItem
from appitem.models import AppService
from utils.utils import listToStr,listToStr2
from utils.jsonhelp import complexObj2json 
# 获取chart 编号
def getChartId(request):
    if request.GET:
        app_id = request.GET.get('app_id')
        host = request.GET.get('host')
        monitor_id = request.GET.get('monitor_id')
        show_type = request.GET.get('show_type')
        res = Chart.objects.filter(app_id=app_id,host_ip=host,monitor_item_id=monitor_id,show_type=show_type,status=1)
        return HttpResponse(res[0].id)
    return  HttpResponseBadRequest("错误请求")

# 获取数据源信息
def getChartInfo(request):
    if request.GET:
        chart_id = request.GET.get('chart_id')
        chart = Chart.objects.get(id = chart_id)
        res = ChartExtend()
        res.host_ip = chart.host_ip
        res.app_name = chart.app_name
        res.monitor_item_id = chart.monitor_item_id
        return HttpResponse(json.dumps(complexObj2json(res)))
    return  HttpResponseBadRequest("错误请求")

# 根据应用中监控项的变化同步show_chart表中的记录   
def sync_chart(app_id):
#1. 当前应用项和监控项情况 
    #此应用对应的监控项
    monitorItem_objects = MonitorItem.objects.filter(app_id = app_id)
    id_list1 = [item.id for item in monitorItem_objects]
    #获取表AppService中的iplist
    app = AppService.objects.get(id = app_id)
    # 防止同一个IP被书写多次
    ip_set1 = set(app.ip_list.split(","))
    #应用名
    app_name = app.app_name
    
    
    ds_set1= set()
    for mid in id_list1:
        for ip in ip_set1:
            ds_set1.add(str(mid) + "," + ip)
    

#2. 当前show_chart表中的情况
    #取出当前show_chart数据表里的所有monitor_item_id
    chart_objects = Chart.objects.filter(app_name = app_name,status=1)
    
    ds_set2= set()
    for chart in chart_objects:
        ds_set2.add(str(chart.monitor_item_id) + "," + chart.host_ip)
 
#3. 计算差异，并同步          
    # 需要新增加的数据源
    # 监控项id和ip的组合构成了一个数据源
    diff_insert = ds_set1 - ds_set2
    
    # 需要删除的数据源  
    diff_delete = ds_set2 - ds_set1

    #如果差集存在，则取出所有chart表中没有的的id和ip插入表chart
    for item in diff_insert:
        id_ip = item.split(",")
        monitor_item_id = int(id_ip[0])
        host_ip = id_ip[1]
        for show_type in range(1,5):
            Chart(monitor_item_id = monitor_item_id, host_ip = host_ip, show_type = show_type, app_name = app_name, status = 1, app_id = app_id).save()

   
    ##如果差集存在，则取出chart表中对应的记录，将status置为0
    if diff_delete:
        monitor_item_idlist = []
        host_iplist = []
        for item in diff_delete:
            id_ip = item.split(",")
            monitor_item_id = int(id_ip[0])
            host_ip = id_ip[1]
            monitor_item_idlist.append(monitor_item_id)
            host_iplist.append(host_ip)
        Chart.objects.extra(where=['monitor_item_id IN (' + listToStr(monitor_item_idlist) + ')' , 'host_ip IN (' + listToStr2(host_iplist) + ')']).update(status = 0)

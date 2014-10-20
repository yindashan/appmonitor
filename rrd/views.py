#!usr/bin/env python
# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import *
from django.contrib.auth import authenticate, login as auth_login , logout as auth_logout
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.conf import settings

#standard library
import time
import json
import random

#our own code
from utils.utils import genRRDPath
from rrd.models import fetch_rrd


#返回图表展示所需的监控项数据
#从请求中提取参数 1)ip --- IP地址  2)app --- 应用名称   3)dsname  ---- 数据源名称 4)resolution 数据点的时间间隔 5)start 开始时间　6)结束时间

#模拟一批数据    
def chartdata2(request):
    if request.GET:
#        ip = request.GET.get('ip')
#        app = request.GET.get('app')
#        dsname = request.GET.get('dsname')
        resolution = request.GET.get('resolution')
        start = request.GET.get('start')
        end = request.GET.get('end')
        
        if resolution:
            resolution = int(resolution)
        else:
            resolution = 60*5
            
        if end:
            end = int(end)
        else:
            end = int(time.time())
            
        if start:
            start = int(start)
        else:
            start = end - 60*60*4
        cdp_list = []
        while start < end:
            item = {}
            item["time"]=start
            item["value"]=float(random.randint(0,50))
            cdp_list.append(item)
            start += resolution
        return HttpResponse(content=json.dumps(cdp_list), content_type='text/plain')
    return  HttpResponseBadRequest("错误请求")
    
def chartdata(request):
    if request.GET:
        #1. 处理参数
        ip = request.GET.get('ip')
        app = request.GET.get('app')
        dsname = request.GET.get('dsname')
        resolution = request.GET.get('resolution')
        start = request.GET.get('start')
        end = request.GET.get('end')
        
        if resolution:
            resolution = int(resolution)
        else:
            resolution = 60*5
            
        if end:
            end = int(end)
        else:
            end = int(time.time())
            
        if start:
            start = int(start)
        else:
            start = end - 60*60*4
            
        #2.1组装rrd文件和xml文件路径
        rrd_file_path = genRRDPath(settings.PERFDATA_PATH, ip, app, dsname)
        
        #2.2 从rrd文件中提取cdp数据   CDP（consolidated data point）
        cdp_list = []
        # 由于每一个监控项的数据单独存储在一个文件中，因此数据源的标示唯一
        ds = '1';
        try:
            cdp_list = fetch_rrd(rrd_file_path, ds, start, end, resolution)
        except BaseException, e:
            return  HttpResponseBadRequest("错误请求" + str(e))
        return HttpResponse(content=json.dumps(cdp_list), content_type='text/plain')
    return  HttpResponseBadRequest("错误请求")
    
    
# 精确数据值,直接从1分钟的数据环上取数据
# 注意要考虑到 heartbeat 的影响
# 目前此值　ds[1].minimal_heartbeat = 8460
def precisedata(request):
    if request.GET:
        #1. 处理参数
        ip = request.GET.get('ip')
        app = request.GET.get('app')
        dsname = request.GET.get('dsname')
        resolution = 60
        start = request.GET.get('start')
        end = request.GET.get('end')
        
        if end:
            end = int(end)
        else:
            end = int(time.time())
            
        if start:
            start = int(start)
        else:
            start = end - 60*60*4
            
        #2.1组装rrd文件和xml文件路径
        rrd_file_path = genRRDPath(settings.PERFDATA_PATH, ip, app, dsname)
        
        #2.2 从rrd文件中提取cdp数据   CDP（consolidated data point）
        cdp_list = []
        # 由于每一个监控项的数据单独存储在一个文件中，因此数据源的标示唯一
        ds = '1';
        try:
            cdp_list = fetch_rrd(rrd_file_path, ds, start, end, resolution)
        except BaseException, e:
            return  HttpResponseBadRequest("错误请求" + str(e))
            
        # 把以秒为单位的时间转换为人类可读的时间
        for item in cdp_list:
            item['time'] = time.strftime('%Y-%m-%d %H:%M',time.localtime(item['time']))
            
        return HttpResponse(content=json.dumps(cdp_list), content_type='text/plain')
    return  HttpResponseBadRequest("错误请求")



  
    
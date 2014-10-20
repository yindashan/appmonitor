#!usr/bin/env python
# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import *
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from utils.constants import alarm_type_dict


# stdandard library
import json

# 导入在forms.py 中定义的所有表单类。
from appitem.models import AppService 
from monitoritem.models import MonitorItem,monitorItem2Extend2
from showchart.models import Chart
from showchart.views import sync_chart
from authority.models import app2AuthStr
from authority.models import Permission
from log.models import Log
from utils.utils import listToStr2,listToStr
from combinechart.models import CombineChart
from utils.jsonhelp import complexObj2json
from combinechart.models import combine2Extend

##显示应用列表
@login_required
def index(request):
    item_list = AppService.objects.order_by('-id')
    auth_set = request.session["authority_set"]
    apps = []
    for item in item_list:
        if app2AuthStr(item.app_name,'operate') in auth_set:
            apps.append(item)
    paginator = Paginator(apps, 10)
    currentPage = request.POST.get('pageNum',1)
    try:
        pager = paginator.page(currentPage)
    except InvalidPage:
        pager = paginator.page(1)
    # 页面表格单元格太长
    deal_comma(pager.object_list)
    return render_to_response('appitem/index.html',{'app_list':pager, 'alarm_type_dict':alarm_type_dict, 'auth_set':request.session["authority_set"]}, context_instance=RequestContext(request))

##删除记录
@login_required
def delete(request, app_id):
    app = None
    try:
        app = AppService.objects.get(id=int(app_id))
    except BaseException:
        return HttpResponse(simplejson.dumps({"statusCode":400, "message":u'应用项不存在!'}), mimetype='application/json')
    #删除应用对应的监控项
    mitems = MonitorItem.objects.filter(app=app.id)
    #查找show_chart表中记录，将此应用对应的记录的status改为0
    Chart.objects.filter(app_id = app_id).update(status = 0)
    mitems.delete()
    app.delete()
    # 删除此应用对应的权限字段
    Permission.objects.get(codename=app2AuthStr(app.app_name,"read")).delete()
    Permission.objects.get(codename=app2AuthStr(app.app_name,"operate")).delete()
    # 日志
    Log(username=request.user.username,log_type=3,relate_id=app.id,content="execute delete appitem " + app.app_name + " success!", level=1).save()
    return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/appitem/index", "message":u'删除成功'}), mimetype='application/json')

@login_required
def add(request):
    if request.POST:

        app_name = request.POST.get('app_name')
        #清除左右两侧空格
        app_name = app_name.strip()
        desc = request.POST.get('desc')
        ip_list = request.POST.get('ip_list')
        check_interval = request.POST.get('check_interval')
        max_check_attempts = request.POST.get('max_check_attempts')
        # 过滤IP列表防止出现重复的IP地址        
        ip_list = filterIP(ip_list)
        email_list = request.POST.get('email_list', None)
        mobile_list = request.POST.get('mobile_list', None)
        if email_list or mobile_list:
            alarmtype = 1
        else:
            alarmtype = 0
        #验证重复应用名
        app = AppService.objects.filter(app_name__iexact=app_name)
        if app:
            return HttpResponse(simplejson.dumps({"statusCode":400, "message":u'应用服务记录已经存在不能添加'}), mimetype='application/json')

        else:
            newapp = AppService(app_name=app_name, desc=desc, ip_list=ip_list, \
            email_list=email_list,mobile_list=mobile_list,alarmtype=alarmtype, \
            check_interval=check_interval,max_check_attempts=max_check_attempts )
            newapp.save()
            # 创建对应的权限记录 此应用监控项的读和操作权限
            newpm = Permission();
            newpm.codename = app2AuthStr(app_name,"read")
            newpm.desc = app_name + u"监控项读权限"
            newpm.type=3
            newpm.save()
            
            newpm = Permission()
            newpm.codename = app2AuthStr(app_name,"operate")
            newpm.desc = app_name + u"监控项操作权限"
            newpm.type=3
            newpm.save()
            # 日志
            Log(username=request.user.username,log_type=3,relate_id=newapp.id,content="execute add appitem " + newapp.app_name + " success!", level=1).save()
            return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/appitem/index", "message":u'添加成功'}), mimetype='application/json')
    return render_to_response('appitem/add.html',context_instance=RequestContext(request)) 

@login_required
def edit(request, app_id):
    app = None
    try:
        app = AppService.objects.get(id=int(app_id))
    except BaseException:
        return HttpResponse(simplejson.dumps({"statusCode":400, "message":u'应用项不存在!'}), mimetype='application/json')
    if request.POST:
        app.desc = request.POST.get('desc')
        ip_list = request.POST.get('ip_list')
        app.check_interval = request.POST.get('check_interval')
        app.max_check_attempts = request.POST.get('max_check_attempts')
        
        # 过滤IP列表防止出现重复的IP地址        
        app.ip_list = filterIP(ip_list)
        app.email_list = request.POST.get('email_list', None)
        app.mobile_list = request.POST.get('mobile_list', None)
        if app.email_list or app.mobile_list:
            app.alarmtype = 1
        else:
            app.alarmtype = 0
        app.save()
        
        #如果应用项ip列表变化，则改变show_chart表,将新的ip插入到chart表,减少的ip对应的status置0
        sync_chart(app_id)
        
        # 日志
        Log(username=request.user.username,log_type=3,relate_id=app.id,content="execute edit appitem " + app.app_name + " success!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/appitem/index", "message":u'编辑成功'}), mimetype='application/json')  
    return render_to_response('appitem/edit.html', {'app': app})

@login_required
def selecteddel(request):
    ids = request.POST.get('ids', None)
    if ids:
        apps = AppService.objects.extra(where=['id IN (' + ids + ')'])
        if not apps:
            return HttpResponse(simplejson.dumps({"statusCode":400,"url": "/appitem/index", "message":u'选中应用服务不存在不能批量删除'}), mimetype='application/json')
        
        app_str = ""
        for app in apps:
            app_str +=(" "+app.app_name)
            # 删除应用对应的监控项
            mitems = MonitorItem.objects.filter(app=app.id)
            
            #查找show_chart表中记录，将此应用对应的记录的status改为0
            Chart.objects.filter(app_id = app.id).update(status = 0)
        mitems.delete()
        # 删除应用对应的权限
        code_list = []
        for app in apps:
            code_list.append(app2AuthStr(app.app_name,"read"))
            code_list.append(app2AuthStr(app.app_name,"operate"))
        Permission.objects.extra(where=['codename IN (' + listToStr2(code_list) + ')']).delete()
        
        # 日志
        Log(username=request.user.username,log_type=3,content="execute selecteddel appitem " + app_str + " success!", level=1).save()
        # 删除应用项
        apps.delete()
    return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/appitem/index", "message":u'删除成功'}), mimetype='application/json')
        
# 供页面ajax请求使用
def getappinfo(request):
    if request.POST:
        app_id = int(request.POST.get("app_id"))
        app = AppService.objects.get(id = app_id);
        host_list = app.ip_list.split(',')
        monitor_item_list = MonitorItem.objects.filter(app_id=app_id)
        monitor_list = monitorItem2Extend2(monitor_item_list)
        #monitor_list = monitorItem2Extend(auth_set,monitor_item_list)
        dd = {}
        dd["host_list"] = host_list
        dd["monitor_list"] = complexObj2json(monitor_list)
        return HttpResponse(json.dumps(dd))
    else:
        return  HttpResponseBadRequest("错误请求")

# 获取应用项对应的联合图
def getAppCombineChart(request):
    if request.POST:
        app_id = int(request.POST.get("app_id"))
        chart_list = CombineChart.objects.filter(app_id=app_id)
        chart_list = combine2Extend(chart_list)
        return HttpResponse(json.dumps(complexObj2json(chart_list)))
    else:
        return  HttpResponseBadRequest("错误请求")
        
# 过滤IP列表防止出现重复的IP地址        
def filterIP(ip_list_str):
    ip_list = list(set(ip_list_str.split(',')))
    ip_list.sort()
    return listToStr(ip_list)

def deal_comma(app_list):
    for app in app_list:
        ips = app.ip_list.split(",")
        res = ""
        for i in range(len(ips)):
            res += ips[i]
            if i != len(ips) - 1:
                res += ','
            if (i + 1) % 5 == 0:
                res += "\n"
        app.ip_list = res


  
    

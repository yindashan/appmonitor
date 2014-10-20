#!usr/bin/env python
# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import *
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson
from django.core.paginator import Paginator, InvalidPage, EmptyPage,PageNotAnInteger
from django.contrib.auth.decorators import login_required



# 导入在forms.py 中定义的所有表单类。
from monitoritem.models import MonitorItem 
from monitoritem.models import generate_threshold
from monitoritem.models import parse_threshold
from monitoritem.models import monitorItem2Extend
from appitem.models import AppService
from utils.utils import listToStr
from showchart.models import Chart
from showchart.views import sync_chart
from authority.models import app2AuthStr
from authority.models import hasMonitorAuth,get_readable_app
from log.models import Log


#显示应用列表
@login_required
def index(request):
    # 部分应用中监控项读权限
    auth_set = request.session["authority_set"]
    app_id_list = get_readable_app(request)
    
    # 具有读权限的应用
    app_list = AppService.objects.filter(id__in = app_id_list).order_by('id')
    
    
    if not app_id_list:
        return HttpResponse("你可能没有此功能的访问权限,请重新登录!")
        
    ids = listToStr(app_id_list)
    items = MonitorItem.objects.extra(where=['app_id IN (' + ids + ')']).order_by('-id')

    paginator = Paginator(items, 10)
    currentPage = request.POST.get('pageNum',1)
    try:
        pager = paginator.page(currentPage)
    except InvalidPage:
        pager = paginator.page(1)
        
    # 使用MonitorItem的扩展类进行页面显示
    pager.object_list = monitorItem2Extend(auth_set,pager.object_list)
    # 是否有监控项操作权限
    monitor_operate_flag = hasMonitorAuth(auth_set,"operate") 
    return render_to_response('monitoritem/index.html', {'monitoritems':pager, 'monitor_operate_flag':monitor_operate_flag, 'app_list':app_list})

#删除记录
@login_required
def delete(request, item_id):
    try:
        item = MonitorItem.objects.get(id=int(item_id))
    except BaseException:
        return HttpResponse(simplejson.dumps({"statusCode":400, "message":u'监控项不存在!'}), mimetype='application/json')
    item.delete()
    
    #将所有被删除的desc对应的Chart中status置0
    Chart.objects.filter(monitor_item_id = item_id).update(status = 0)
    
    # 日志
    Log(username=request.user.username,log_type=4,relate_id=item.id,content="execute delete monitoritem " + item.app.app_name + " " + item.desc + " success!", level=1).save()
    return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/monitoritem/index", "message":u'删除成功'}), mimetype='application/json')

@login_required
def add(request):
    # 部分应用中监控项读权限
    auth_set = request.session["authority_set"]
    app_list = []
    service_list = AppService.objects.all();
    for service in service_list:
        if app2AuthStr(service.app_name,'operate') in auth_set:
            app_list.append(service)
            
    if request.POST:
        monitor_type = request.POST.get('monitor_type')
        var_name = request.POST.get('var_name')
        # 去除空格
        var_name = var_name.strip()
        formula = request.POST.get('formula')
        
        warning_type = request.POST.get('warning_type')
        w = request.POST.get('w')
        w1 = request.POST.get('w1')
        w2 = request.POST.get('w2')
        warning_threshold = generate_threshold(warning_type,w,w1,w2)
            
        critical_type = request.POST.get('critical_type')
        c = request.POST.get('c')
        c1 = request.POST.get('c1')
        c2 = request.POST.get('c2')
        critical_threshold = generate_threshold(critical_type,c,c1,c2)
        
        
        
        desc = request.POST.get('desc')
        app_id = request.POST.get('app_id')
        
        mitem = MonitorItem(monitor_type=monitor_type, var_name=var_name, formula=formula,warning_threshold=warning_threshold,critical_threshold=critical_threshold,desc=desc,app_id=app_id)
        mitem.save()

        #　根据监控项变化情况，同步show_chart表中的记录
        sync_chart(app_id)
        # 日志
        Log(username=request.user.username,log_type=4,relate_id=mitem.id,content="execute add monitoritem " + mitem.app.app_name + " " + mitem.desc + " success!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/monitoritem/index", "message":u'添加成功'}), mimetype='application/json')        
    return render_to_response('monitoritem/add.html',{'app_list':app_list},context_instance=RequestContext(request)) 

@login_required
def edit(request, item_id):
    app_list = AppService.objects.all()
    try:
        item = MonitorItem.objects.get(id=int(item_id))
    except BaseException:
        return HttpResponse(simplejson.dumps({"statusCode":400, "message":u'监控项不存在!'}), mimetype='application/json')
    warning_tuple = parse_threshold(item.warning_threshold)
    critical_tuple = parse_threshold(item.critical_threshold)
    if request.POST:
        item.monitor_type = request.POST.get('monitor_type')
        item.var_name = request.POST.get('var_name')
        # 去除空格
        item.var_name = item.var_name.strip()
        item.formula = request.POST.get('formula')

        warning_type = request.POST.get('warning_type')
        w = request.POST.get('w')
        w1 = request.POST.get('w1')
        w2 = request.POST.get('w2')
        item.warning_threshold = generate_threshold(warning_type,w,w1,w2)
           
        critical_type = request.POST.get('critical_type')
        c = request.POST.get('c')
        c1 = request.POST.get('c1')
        c2 = request.POST.get('c2')
        item.critical_threshold = generate_threshold(critical_type,c,c1,c2)

        item.desc = request.POST.get('desc')

        item.save()
        
        # 日志
        Log(username=request.user.username,log_type=4,relate_id=item.id,content="execute edit monitoritem " + item.app.app_name + " " + item.desc + " success!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/monitoritem/index", "message":u'编辑成功'}), mimetype='application/json')    
    return render_to_response('monitoritem/edit.html',{'app_list':app_list,'item':item,'warning_tuple':warning_tuple,'critical_tuple':critical_tuple})
    
@login_required
def selecteddel(request):
    ids = request.POST.get('ids', None)
    if ids:
        items = MonitorItem.objects.extra(where=['id IN (' + ids + ')'])
        if not items:
            return HttpResponse(simplejson.dumps({"statusCode":400,"url": "/monitoritem/index", "message":u'选中监控项服务不存在不能批量删除'}), mimetype='application/json')
        item_desc_str = ""
        for item in items:
            # 用于记录日志
            item_desc_str += ('|' + item.app.app_name + ' ' + item.desc + '|')
            Chart.objects.filter(monitor_item_id = item.id).update(status = 0)        
        items.delete()
        # 日志
        Log(username=request.user.username,log_type=4,content="execute selecteddel monitoritem " + item_desc_str + " success!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/monitoritem/index", "message":u'删除成功'}), mimetype='application/json')

@login_required
def search(request):
    # 具有读权限的应用
    app_id_list = get_readable_app(request)
    
    auth_set = request.session["authority_set"]
    
    if not app_id_list:
        return HttpResponse(simplejson.dumps({"statusCode":400, "message":u'你可能没有此功能的访问权限!'}), mimetype='application/json')
        
    if request.POST:
        app_id = request.POST.get("app_id")
        query = request.POST.get("query")
        
        items = MonitorItem.objects.filter(app_id__in = app_id_list).order_by('-id')
        
        if app_id:
            app_id = int(app_id)
            items = items.filter(app_id=app_id)
        if query:
            items = items.filter(desc__icontains = query)
            
        paginator = Paginator(items, 10)
        currentPage = request.POST.get('pageNum',1)
        try:
            pager = paginator.page(currentPage)
        except InvalidPage:
            pager = paginator.page(1)
            
        # 使用MonitorItem的扩展类进行页面显示
        pager.object_list = monitorItem2Extend(auth_set,pager.object_list)
        # 是否有监控项操作权限
        monitor_operate_flag = hasMonitorAuth(auth_set,"operate") 
        return render_to_response('monitoritem/searchback.html', {'monitoritems':pager, 'monitor_operate_flag':monitor_operate_flag})
    else:
        return  HttpResponseBadRequest("错误请求")
    



  
    

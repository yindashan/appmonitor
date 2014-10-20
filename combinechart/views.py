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
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required


import json

# our own code
from authority.models import app2AuthStr
from combinechart.models import CombineChart,combine2Extend,getCombineChartExtend
from appitem.models import AppService
from authority.models import getAppListCanRead,get_readable_app
from utils.constants import show_type_dict
from utils.constants import combine_type_dict
from showchart.models import Chart
from shownode.models import getCombineRealtion
from utils.jsonhelp import complexObj2json
from utils.utils import listToStr

##显示应用列表
@login_required
def index(request):
    # 部分应用中监控项读权限
    app_id_list =  get_readable_app(request)

    if not app_id_list:
        return HttpResponse("你可能没有此功能的访问权限,请重新登录!")
        
    # 具有读权限的应用
    app_list = AppService.objects.filter(id__in = app_id_list).order_by('id')
    
    ids = listToStr(app_id_list)        
    charts = CombineChart.objects.extra(where=['app_id IN (' + ids + ')']).order_by('-id')
    paginator = Paginator(charts, 10)
    currentPage = request.POST.get('pageNum',1)
    try:
        pager = paginator.page(currentPage)
    except InvalidPage:
        pager = paginator.page(1)
        
    pager.object_list = combine2Extend(pager.object_list)
    return render_to_response('combinechart/index.html',{'chart_list':pager,'auth_set':request.session["authority_set"],'app_list':app_list})
 
# 搜索
@login_required
def search(request):
    app_id_list =  get_readable_app(request)
    
    if request.POST:
        app_id = request.POST.get("app_id")
        query = request.POST.get("query")
        
        items = CombineChart.objects.filter(app_id__in = app_id_list).order_by('-id')
        
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
        
        pager.object_list = combine2Extend(pager.object_list)
        return render_to_response('combinechart/searchback.html',{'query':query,'chart_list':pager,'auth_set':request.session["authority_set"]}, context_instance=RequestContext(request))    
    else:
        return  HttpResponseBadRequest("错误请求")
# add
@login_required
def add(request):
    # 部分应用中监控项读权限
    auth_set = request.session["authority_set"]
    app_list = getAppListCanRead(auth_set)
    if request.POST:
        desc = request.POST.get("desc")
        combine_type = request.POST.get("combine_type")
        #print 'combine_type',combine_type
        id_list = request.POST.getlist("chart_ids")
        
        combineChart = CombineChart()
        combineChart.desc = desc
        combineChart.type = int(combine_type)
        #print id_list;
        if id_list:
            chart = Chart.objects.get(id=id_list[0])
            combineChart.app = AppService.objects.get(id=chart.app_id)
        else:
            return HttpResponse(simplejson.dumps({"statusCode":400,"message":u'此联合图对应的数据源不能为空!'}), mimetype='application/json')
        combineChart.save()
        
        # 与showchart 表中记录的关联关系
        for item in id_list:
            combineChart.charts.add(int(item))
        
        return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/combinechart/index", "message":u'添加成功'}), mimetype='application/json')
    return render_to_response('combinechart/add.html',{'show_type_dict':show_type_dict,'combine_type_dict':combine_type_dict,'app_list':app_list}, context_instance=RequestContext(request)) 

# edit
@login_required
def edit(request, item_id):
    # 部分应用中监控项读权限
    auth_set = request.session["authority_set"]
    app_list = getAppListCanRead(auth_set)
    
    combineChart = None
    try:
        combineChart = CombineChart.objects.get(id = int(item_id))
    except BaseException:
        return HttpResponse(simplejson.dumps({"statusCode":400,"message":u'此联合图记录不存在'}), mimetype='application/json')
    chart_list = getCombineRealtion(combineChart);
    if request.POST:
        desc = request.POST.get("desc")
        combine_type = request.POST.get("combine_type")
        #print 'combine_type',combine_type
        id_list = request.POST.getlist("chart_ids")
        
        combineChart = CombineChart.objects.get(id = item_id)
        combineChart.desc = desc
        combineChart.type = int(combine_type)
        #print id_list;
        if id_list:
            chart = Chart.objects.get(id=id_list[0])
            combineChart.app = AppService.objects.get(id=chart.app_id)
        else:
            return HttpResponse(simplejson.dumps({"statusCode":400,"message":u'此联合图对应的数据源不能为空!'}), mimetype='application/json')
            
        combineChart.save()
        
        # 与showchart 表中记录的关联关系
        combineChart.charts.clear()
        for item in id_list:
            combineChart.charts.add(int(item))
        
        return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/combinechart/index", "message":u'编辑成功'}), mimetype='application/json')    
    return render_to_response('combinechart/edit.html',{'show_type_dict':show_type_dict,'combine_type_dict':combine_type_dict,'app_list':app_list,'combineChart':combineChart,'chart_list':chart_list},context_instance=RequestContext(request))

##删除记录
@login_required
def delete(request, item_id):
    combineChart = None
    try:
        combineChart = CombineChart.objects.get(id = int(item_id))
    except BaseException:
        return HttpResponse(simplejson.dumps({"statusCode":400,"message":u'此联合图记录不存在'}), mimetype='application/json')
    # 清除对应关系
    combineChart.charts.clear()
    combineChart.delete()
    return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/combinechart/index", "message":u'删除成功'}), mimetype='application/json')

@login_required
def selecteddel(request):
    ids = request.POST.get('ids', None)
    if ids:
        combineCharts = CombineChart.objects.extra(where=['id IN (' + ids + ')'])
        if not combineCharts:
            return HttpResponse(simplejson.dumps({"statusCode":400,"message":u'选中的联合图不存在不能批量删除'}), mimetype='application/json')
        for item in combineCharts:
            # 删除关联关系
            item.charts.clear()
            item.delete()
    return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/combinechart/index", "message":u'删除成功'}), mimetype='application/json')
    
@login_required   
def getCombineChart(request):
    combine_id = request.POST.get("combine_id")
    combineChart = getCombineChartExtend(int(combine_id))
    return HttpResponse(json.dumps(complexObj2json(combineChart)), mimetype='application/json')
    

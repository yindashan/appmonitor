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


# stdandard library
import json
import datetime

# our own code
from servicegroup.models import ServiceGroup
from caseset.models import CaseSet,Case,JudgeRule,CaseExtend
from checkresult.models import Task
from log.models import Log   
from product.models import Product,get_usable_product
 

# 显示列表
@login_required
def index(request):
    # 能够操作的产品
    product_id_list = get_usable_product(request)
    
    item_list = CaseSet.objects.filter(product_id__in = product_id_list).order_by('-id')
    paginator = Paginator(item_list, 10)
    currentPage = request.POST.get('pageNum', 1)
    try:
        pager = paginator.page(currentPage)
    except InvalidPage:
        pager = paginator.page(1)
    
    return render_to_response('caseset/index.html',{'item_list':pager}, context_instance=RequestContext(request))

# 删除记录
@login_required
def delete(request, set_id):
    caseset = None
    try:
        caseset = CaseSet.objects.get(id=int(set_id))
    except BaseException:
        return HttpResponse(simplejson.dumps({"statusCode":400, "message":u'测试集不存在!'}), mimetype='application/json')
    # delete
    # 1) 测试用例
    items = Case.objects.filter(case_set_id=caseset.id)
    items.delete()
    # 2) 测试集和服务集群关联关系
    caseset.service_groups.clear()
    # 3) 测试集合
    caseset.delete()

    # 日志
    Log(username=request.user.username,log_type=7,relate_id=caseset.id,content="execute delete case_set " + caseset.name + " success!", level=1).save()
    return HttpResponse(simplejson.dumps({"statusCode":200, "url": "/caseset/index", "message":u'删除成功'}), mimetype='application/json')

@login_required
def add(request):
    if request.method == 'POST':
        product_id = int(request.POST.get('product'))
        name = request.POST.get('name')
        comment = request.POST.get('comment')
        case_list = request.POST.get('obj_list');
        item_list = json.loads(case_list)
        group_id_list = request.POST.getlist("service_group")
        #print '--------------------------------',group_id_list

        # 保存 服务组信息
        caseset = CaseSet()
        caseset.product = Product.objects.get(id=product_id)
        caseset.name = name
        caseset.comment = comment
        caseset.save()

        # 保存 单个服务信息
        for item in item_list:
            t = Case()
            t.url = item['url']
            t.comment = item['comment']
            t.rule = JudgeRule.objects.get(id=item['rule_id'])
            t.params = item['params']
            t.case_set = caseset
            t.save()

        # 测试集和服务集群关联关系
        for gid in group_id_list:
            caseset.service_groups.add(gid) 
 
        # 日志
        Log(username=request.user.username, log_type=7, content="execute add case_set " + caseset.name + " success!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/caseset/index", "message":u'添加成功'}), mimetype='application/json')
    else:
        rule_list = JudgeRule.objects.all();
        # 能够操作的产品
        product_id_list = get_usable_product(request)
        # 此产品的所有服务集群
        group_list = ServiceGroup.objects.filter(product_id__in = product_id_list)
        
        # 产品列表
        product_list = Product.objects.filter(id__in = product_id_list)
        
        return render_to_response('caseset/add.html', {'rule_list':rule_list,'group_list':group_list,'product_list':product_list}, context_instance=RequestContext(request)) 

@login_required
def edit(request, set_id):
    caseset = None
    try:
        caseset = CaseSet.objects.get(id=int(set_id))
    except BaseException:
        return HttpResponse(simplejson.dumps({"statusCode":400, "message":u'测试集不存在!'}), mimetype='application/json')

    if request.method == 'POST':
        group_id_list = request.POST.getlist("service_group")
        # 保存 服务组信息
        product_id = int(request.POST.get('product'))
        caseset.product = Product.objects.get(id=product_id)
        caseset.name = request.POST.get('name')
        caseset.comment = request.POST.get('comment')
        caseset.save()

        # 保存新增服务信息
        case_list = request.POST.get('obj_list');
        item_list = json.loads(case_list)

        # 保存 单个服务信息
        for item in item_list:
            t = Case()
            t.url = item['url']
            t.comment = item['comment']
            t.rule = JudgeRule.objects.get(id=item['rule_id'])
            t.params = item['params']
            t.case_set = caseset
            t.save()

        # 删除某些服务项
        ids = request.POST.get('ids')
        if ids:
            items = Case.objects.extra(where=['id IN (' + ids + ')'])
            items.delete();

        # 测试集和服务集群关联关系
        caseset.service_groups.clear()
        for gid in group_id_list:
            caseset.service_groups.add(gid) 

        # 日志
        Log(username=request.user.username,log_type=7,relate_id=caseset.id,content="execute edit case_set " + caseset.name + " success!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/caseset/index", "message":u'编辑成功'}), mimetype='application/json')
    else:  
        # rule
        rule_list = JudgeRule.objects.all();
        # case
        case_list = Case.objects.filter(case_set_id = set_id)
        
        case_list = change_case(case_list)
        
        # 此产品的所有服务集群
        product_id_list = get_usable_product(request)
        group_list = ServiceGroup.objects.filter(product_id__in = product_id_list)
        # 已选定的群组
        group_id_list = [ item.id for item in caseset.service_groups.all()]
        
        # 产品列表
        product_list = Product.objects.filter(id__in = product_id_list)
        
        return render_to_response('caseset/edit.html', {'caseset':caseset,'rule_list':rule_list,'case_list':case_list,\
            'group_list':group_list,'group_id_list':group_id_list,'product_list':product_list})

@login_required
def selecteddel(request):
    ids = request.POST.get('ids')
    if ids:
        sets = CaseSet.objects.extra(where=['id IN (' + ids + ')'])
        if not sets:
            return HttpResponse(simplejson.dumps({"statusCode":400, "message":u'选中的组不存在,不能批量删除'}), mimetype='application/json')
        
        temp = ""
        for item in sets:
            temp +=("|"+item.name)

        # 删除
        # 1) 删除测试用例
        items = Case.objects.extra(where=['case_set_id IN (' + ids + ')'])
        items.delete() 
        # 2) 测试集和服务集群关联关系
        for caseset in sets:
            caseset.service_groups.clear()
        # 3) 删除测试集合
        sets.delete()

        # 日志
        Log(username=request.user.username,log_type=7,content="execute selecteddel case_set " + temp + " success!", level=1).save()
    return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/caseset/index", "message":u'删除成功'}), mimetype='application/json')
                
def change_case(item_list):
    res = []
    for item in item_list:
        temp = CaseExtend(item)
        if len(temp.url) > 40:
            temp.url = temp.url[0:37] +'...'
        if temp.comment and len(temp.comment)> 25:
            temp.comment = temp.comment[0:22] +'...'
        res.append(temp)
    return res

# 使用测试集对目标服务集群进行测试    
@login_required
def execute(request, set_id):
    caseset = CaseSet.objects.get(id = set_id)
    
    t = Task()
    t.set_id = set_id
    t.product = caseset.product.product_name
    # 0:初始 1:处理中 2:执行完成
    t.status = 0
    t.comment = caseset.comment
    t.create_time = datetime.datetime.now()
    # 未通过
    t.is_pass = 0
    t.save()
    return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/checkresult/index", "message":u'任务提交成功，请在3分钟后,查看检查结果'}), mimetype='application/json')

        
    

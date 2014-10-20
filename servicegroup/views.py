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

# our own code
from servicegroup.models import ServiceGroup,ServiceItem,ServiceItemExtend
from utils.constants import idc_dict,yes_no_dict
from log.models import Log
from caseset.models import CaseSet
from product.models import Product,get_usable_product


# 显示公告列表
@login_required
def index(request):
    product_id_list = get_usable_product(request)
    item_list = ServiceGroup.objects.filter(product_id__in = product_id_list).order_by('-id')
    paginator = Paginator(item_list, 10)
    currentPage = request.POST.get('pageNum', 1)
    try:
        pager = paginator.page(currentPage)
    except InvalidPage:
        pager = paginator.page(1)

    return render_to_response('servicegroup/index.html',{'item_list':pager}, context_instance=RequestContext(request))

# 删除记录
@login_required
def delete(request, group_id):
    group = None
    try:
        group = ServiceGroup.objects.get(id=int(group_id))
    except BaseException:
        return HttpResponse(simplejson.dumps({"statusCode":400, "message":u'服务组不存在!'}), mimetype='application/json')
    # delete
    # 1) 服务集群中的单个服务
    items = ServiceItem.objects.filter(group=group.id)
    items.delete()
    # 2) 测试集和服务集群关联关系
    group.caseset_set.clear()
    # 3) 服务集群
    group.delete()
    # 日志
    Log(username=request.user.username,log_type=6,relate_id=group.id,content="execute delete service_group " + group.name + " success!", level=1).save()
    return HttpResponse(simplejson.dumps({"statusCode":200, "url": "/servicegroup/index", "message":u'删除成功'}), mimetype='application/json')

@login_required
def add(request):
    if request.method == 'POST':
        product_id = int(request.POST.get('product'))
        name = request.POST.get('name')
        comment = request.POST.get('comment')
        service_list = request.POST.get('obj_list');
        caseset_id_list = request.POST.getlist("caseset")
        print '------------------------------------'
        print service_list
        print '------------------------------------'
        item_list = json.loads(service_list)

        # 保存 服务组信息
        sg = ServiceGroup()
        sg.product = Product.objects.get(id=product_id)
        sg.name = name
        sg.comment = comment
        sg.save()

        # 保存 单个服务信息
        for item in item_list:
            t = ServiceItem()
            t.idc = item['idc'] 
            t.ip = item['ip']
            t.port = item['port']
            t.is_use_proxy = item['is_use_proxy']
            t.group = sg
            t.save()
            
        # 测试集和服务集群关联关系
        for cid in caseset_id_list:
            sg.caseset_set.add(cid) 
       
        # 日志
        Log(username=request.user.username, log_type=6, content="execute add service_group " + sg.name + " success!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/servicegroup/index", "message":u'添加成功'}), mimetype='application/json')
    else:
        # 能够操作的产品
        product_id_list = get_usable_product(request)
        caseset_list = CaseSet.objects.filter(product_id__in=product_id_list)
        
        # 产品列表
        product_list = Product.objects.filter(id__in = product_id_list)
        
        return render_to_response('servicegroup/add.html',{'idc_dict':idc_dict,'caseset_list':caseset_list,'product_list':product_list},context_instance=RequestContext(request)) 

@login_required
def edit(request, group_id):
    group = None
    try:
        group = ServiceGroup.objects.get(id=int(group_id))
    except BaseException:
        return HttpResponse(simplejson.dumps({"statusCode":400, "message":u'服务组不存在!'}), mimetype='application/json')

    if request.method == 'POST':
        # 保存 服务组信息
        product_id = int(request.POST.get('product'))
        group.product = Product.objects.get(id=product_id)
        group.name = request.POST.get('name')
        group.comment = request.POST.get('comment')
        group.save()

        # 保存新增服务信息
        service_list = request.POST.get('obj_list');
        item_list = json.loads(service_list)


        # 保存 单个服务信息
        for item in item_list:
            t = ServiceItem()
            t.idc = item['idc'] 
            t.ip = item['ip']
            t.port = item['port']
            t.is_use_proxy = item['is_use_proxy']
            t.group = group
            t.save()

        # 删除某些服务项
        ids = request.POST.get('ids')
        if ids:
            items = ServiceItem.objects.extra(where=['id IN (' + ids + ')'])
            items.delete();
            
        # 测试集和服务集群关联关系
        caseset_id_list = request.POST.getlist("caseset")
        group.caseset_set.clear()
        for cid in caseset_id_list:
            group.caseset_set.add(cid) 

        # 日志
        Log(username=request.user.username,log_type=6,relate_id=group.id,content="execute edit service_group " + group.name + " success!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/servicegroup/index", "message":u'编辑成功'}), mimetype='application/json')
    else:  
        service_list = ServiceItem.objects.filter(group=group).extra(select={'ipa': "inet_aton(ip)"}).order_by('idc','ipa')
        service_list = change(service_list)
        
        # 能够操作的产品
        product_id_list = get_usable_product(request)
        
        caseset_list = CaseSet.objects.filter(product_id__in=product_id_list)
        
        # 已选定的测试集
        caseset_id_list = [ item.id for item in group.caseset_set.all()]
        # 产品列表
        product_list = Product.objects.filter(id__in = product_id_list)
        
        return render_to_response('servicegroup/edit.html', {'group':group,'service_list':service_list,'idc_dict':idc_dict, \
            'caseset_list':caseset_list,'caseset_id_list':caseset_id_list,'product_list':product_list})

@login_required
def selecteddel(request):
    ids = request.POST.get('ids')
    if ids:
        groups = ServiceGroup.objects.extra(where=['id IN (' + ids + ')'])
        if not groups:
            return HttpResponse(simplejson.dumps({"statusCode":400, "message":u'选中的组不存在,不能批量删除'}), mimetype='application/json')
        
        temp = ""
        for item in groups:
            temp +=("|"+item.name)

        # 删除
        # 1) 删除服务项
        items = ServiceItem.objects.extra(where=['group_id IN (' + ids + ')'])
        items.delete()
        # 2) 测试集和服务集群关联关系
        for item in groups:
            item.caseset_set.clear()
        # 3) 删除服务组
        groups.delete()
        # 日志
        Log(username=request.user.username,log_type=4,content="execute selecteddel service_group " + temp + " success!", level=1).save()
    return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/servicegroup/index", "message":u'删除成功'}), mimetype='application/json')
        
def change(item_list):
    ll = []
    for item in item_list:
        temp = ServiceItemExtend(item)
        temp.idc = idc_dict[temp.idc]
        temp.is_use_proxy = yes_no_dict[temp.is_use_proxy]
        ll.append(temp)
    return ll

        
        
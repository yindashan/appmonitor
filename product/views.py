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


# our own code
from product.models import Product
from log.models import Log
from authority.models import Permission, product2AuthStr
from servicegroup.models import ServiceGroup
from caseset.models import CaseSet


# 显示列表
@login_required
def index(request):
    item_list = Product.objects.order_by('id')
    paginator = Paginator(item_list, 10)
    currentPage = request.POST.get('pageNum', 1)
    try:
        pager = paginator.page(currentPage)
    except InvalidPage:
        pager = paginator.page(1)
    
    return render_to_response('product/index.html', {'item_list':pager}, context_instance=RequestContext(request))
    
@login_required
def add(request):
    if request.method == 'POST':
        p = Product()
        p.product_name = request.POST.get('product_name')
        p.save()
        
        # 添加权限记录
        newpm = Permission()
        newpm.codename = product2AuthStr(p.id)
        newpm.desc = p.product_name + u"操作权限"
        newpm.type = 5
        newpm.save()
        
        # 日志
        Log(username=request.user.username, log_type=8, content="execute add product " + p.product_name + " success!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":200, "url": "/product/index", "message":u'添加成功'}), mimetype='application/json')
    else:
        return render_to_response('product/add.html', context_instance=RequestContext(request)) 

# 删除记录
@login_required
def delete(request, product_id):
    product = None
    try:
        product = Product.objects.get(id=int(product_id))
    except BaseException:
        return HttpResponse(simplejson.dumps({"statusCode":400, "message":u'该产品不存在!'}), mimetype='application/json')
    # 删除
    del_product(product)
    # 日志
    Log(username=request.user.username, log_type=8, relate_id=product.id, content="execute delete product " + product.product_name + " success!", level=1).save()
    return HttpResponse(simplejson.dumps({"statusCode":200, "url": "/product/index", "message":u'删除成功'}), mimetype='application/json')
 
# 批量删除   
@login_required
def selecteddel(request):
    ids = request.POST.get('ids')
    if ids:
        products = Product.objects.extra(where=['id IN (' + ids + ')'])
        if not products:
            return HttpResponse(simplejson.dumps({"statusCode":400, "message":u'选中的产品不存在,不能批量删除'}), mimetype='application/json')
        
        temp = []
        for item in products:
            temp.append(item.product_name)
            del_product(item)
        temp = '|'.join(temp)
        
        # 日志
        Log(username=request.user.username,log_type=8,content="execute selecteddel product " + temp + " success!", level=1).save()
    return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/product/index", "message":u'删除成功'}), mimetype='application/json')
  
@login_required
def edit(request, product_id):
    product = None
    try:
        product = Product.objects.get(id=int(product_id))
    except BaseException:
        return HttpResponse(simplejson.dumps({"statusCode":400, "message":u'产品不存在!'}), mimetype='application/json')

    if request.method == 'POST':
        product.product_name = request.POST.get("product_name")
        product.save()
        
        # 日志
        Log(username=request.user.username,log_type=7,relate_id=product.id,content="execute edit product " + product.product_name + " success!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":200,"url": "/product/index", "message":u'编辑成功'}), mimetype='application/json')
    else:  

        return render_to_response('product/edit.html', {'product':product})

def del_product(product):
    # 1) 与产品关联的服务集群
    ServiceGroup.objects.filter(product_id=product.id).delete()
    # 2) 与产品关联的测试集合
    CaseSet.objects.filter(product_id=product.id).delete()
    # 3) 与产品关联的权限
    Permission.objects.filter(codename = product2AuthStr(product.id)).delete()
    # 4) 产品
    product.delete()


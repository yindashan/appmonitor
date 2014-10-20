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
#import json

# our own code
from checkresult.models import CheckResult
from utils.constants import yes_no_dict
from checkresult.models import Task
from utils.constants import task_status_dict,is_pass_dict

# 显示任务列表
@login_required
def index(request):
    item_list = Task.objects.order_by('-create_time')
    paginator = Paginator(item_list, 10)
    currentPage = request.POST.get('pageNum', 1)
    try:
        pager = paginator.page(currentPage)
    except InvalidPage:
        pager = paginator.page(1)
    change(pager.object_list)
    return render_to_response('checkresult/index.html',{'item_list':pager})
    
# 任务详情
def taskdetail(request,task_id):
    task = Task.objects.get(id = task_id)
    task_change(task)
    # 每个测试用例的执行情况
    item_list = CheckResult.objects.filter(task_id = task_id)
    checkresult_change(item_list)
    return render_to_response('checkresult/taskdetail.html',{'task':task, 'item_list':item_list})
    
# 查看检查结果   
def watch(request,result_id):
    item = None
    try:
        item = CheckResult.objects.get(id=int(result_id))
    except BaseException:
        return HttpResponse(simplejson.dumps({"statusCode":400, "message":u'检查结果项不存在!'}), mimetype='application/json')
    
    item.execute_time = item.execute_time.strftime('%Y-%m-%d %H:%M:%S')
    item.is_pass = yes_no_dict[item.is_pass]
    return render_to_response('checkresult/watch.html',{'item':item})
    
def change(item_list):
    for item in item_list:
        # 如果处理完成
        if item.status == 2:
            item.status = task_status_dict[item.status] + ' ' + is_pass_dict[item.is_pass]
        else:
            item.status = task_status_dict[item.status]
        #item.is_pass = is_pass_dict[item.is_pass]
        item.create_time = item.create_time.strftime('%Y-%m-%d %H:%M:%S')
        
def task_change(task):
    task.create_time = task.create_time.strftime('%Y-%m-%d %H:%M:%S')
    task.execute_time = task.execute_time.strftime('%Y-%m-%d %H:%M:%S')
    task.is_pass = is_pass_dict[task.is_pass]
    
def checkresult_change(item_list):
    for item in item_list:
        item.is_pass = is_pass_dict[item.is_pass]
        
        
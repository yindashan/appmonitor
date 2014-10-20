# -*- coding:utf-8 -*-

#django
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
from django.db import connection

#standard library
import json

#our own code
from shownode.models import tree_structure,right_tree_struct  
from shownode.models import ShowChartExtend,ShowNode,getCombineChartBySort
from shownode.models import delete_node,update_node,append_node 
from utils.constants import show_type_dict
from role.models import Role
from combinechart.models import combine2Extend
from utils.jsonhelp import complexObj2json
from shownode.models import getChartlist,getCombineChartlist
from account.models import getUser
from authority.models import getAppListCanRead

#--------------全局变量---------------
control_level = 3

#显示组织机构视图
@login_required
def tree(request):
    #根节点id
    node_id = 1;
    #权限集合
    auth_set = request.session["authority_set"]
    tree_struct = tree_structure(node_id,auth_set,None,control_level)
    node_list = []
    if tree_struct:
        node_list.append(tree_struct)
    return HttpResponse(json.dumps(node_list),mimetype="text/plain",status=200,content_type="text/plain")

# 用于配置读写权限
@login_required
def righttree(request):
    if request.GET:
        return HttpResponseBadRequest("错误请求");
    else:
        purpose = request.POST.get("purpose")
        role_id = request.POST.get("role_id")
        #根节点id
        node_id = 1;
        # 此角色的权限集合
        auth_set = set()
        # 如果编辑一个角色，role_id 不为None
        if role_id != None:
            role = Role.objects.get(id=int(role_id))
            for p in role.permissions.all():
                auth_set.add(p.codename)
                
        tree_struct =  right_tree_struct(node_id,control_level,purpose,auth_set)
        node_list = [tree_struct]
        return HttpResponse(json.dumps(node_list),mimetype="text/plain",status=200,content_type="text/plain")
    
@login_required
def manipulate_tree(request):
    if request.POST:
        dd = {}
        dd['status']='failure'
        action = request.POST.get('action')
        if action == 'append':
            parent_id = request.POST.get("parent_id")
            text = request.POST.get("text")
            id_array_str = request.POST.get("related_ids")
            combine_ids_str = request.POST.get("combine_ids")
            node = append_node(parent_id,text,control_level,id_array_str,combine_ids_str)
            
            dd['node_id']=node.id;
        elif action == 'update':
            node_id = request.POST.get("node_id")
            text = request.POST.get("text")
            id_array_str = request.POST.get("related_ids")
            combine_ids_str = request.POST.get("combine_ids")
            #print '-------------combine_ids_str-------------',combine_ids_str
            update_node(node_id,text,id_array_str,combine_ids_str)
            
        elif action == 'delete':
            node_id = int(request.POST.get('node_id'))
            delete_node(node_id)
        dd['status']='success'
        return HttpResponse(content=json.dumps(dd), content_type='text/plain')
    return HttpResponseBadRequest("错误请求");

# 节点当前已经关联的图表
@login_required
def getCurrRelation(request):
    if request.POST:
        
        node_id = int(request.POST.get("node_id"));
        #　单数据源图
        #使用基础函数访问数据库
        cursor = connection.cursor()
        sql = """select s.desc,c.host_ip,m.desc,c.show_type,c.id from node_chart_relation r,show_chart c,monitor_item m,app_service s 
         where r.show_chart_id = c.id and c.monitor_item_id = m.id and m.app_id = s.id  and r.show_node_id = %s and c.status = 1 order by r.id"""
        param = (node_id)
        cursor.execute(sql, param)
        res = cursor.fetchall()
        chart_list = []
        for item in res:
            chart = ShowChartExtend()
            chart.app_desc = item[0].encode('utf-8')
            chart.host_ip = item[1].encode('utf-8')
            chart.monitor_desc = item[2].encode('utf-8')
            chart.show_type = show_type_dict[item[3]]
            chart.show_chart_id = int(item[4])
            chart_list.append(chart)
        # 多数据源图
        combine_charts = getCombineChartBySort(node_id)
        dd = {}
        dd['single_charts'] = chart_list
        dd['combine_charts'] = combine2Extend(combine_charts)
        return HttpResponse(json.dumps(complexObj2json(dd)))
    return HttpResponseBadRequest("错误请求");  


# 获取node所对应的监控项图表  前台点击节点时触发此函数
@login_required
def getchart(request):
    if request.GET:
        node_id = request.GET.get('node_id',1);
        #print '------------node_id------------',node_id
        chart_list = getChartlist(node_id)
        #print '--------chart_list-------------',len(chart_list)
        combine_list = getCombineChartlist(node_id)
        #print '---------combine_list------------',len(combine_list)
        return render_to_response('showchart/charts.html', {'chart_list': chart_list,'combine_list':combine_list})    
    return  HttpResponseBadRequest("错误请求")

# 展示业务视图页面
@login_required 
def businessview(request):
    if request.method == 'GET':
        node_id = request.GET.get('node_id', 1)
        chart_list = getChartlist(node_id)
        combine_list = getCombineChartlist(node_id)
        
        user = getUser(request.user.id)  
        
        # 部分应用中监控项读权限
        auth_set = request.session["authority_set"]
        # 可以对其监控项进行读操作的应用
        app_list = getAppListCanRead(auth_set)
        
        return render_to_response('showchart/businessview.html', {'user':user,'chart_list': chart_list,\
            'combine_list':combine_list,'app_list':app_list,'show_type_dict':show_type_dict})    
    return  HttpResponseBadRequest("错误请求")
    
    
    
    
    
    

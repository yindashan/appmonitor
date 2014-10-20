# -*- coding:utf-8 -*-
# django library
from django.db import models
from django.contrib.auth.models import User
from appitem.models import AppService

# 权限 每一个权限控制点在此表中表现为一条记录 参看auth_permission
class Permission(models.Model):
    #重新定义表名
    class Meta:
        db_table = 'permission'
    #主键由Django生成
    codename = models.CharField(max_length=64,unique = True) # codename 用于控制  
    desc = models.CharField(max_length=255) # 描述
    #类型 1:用户和角色 2:应用项　相关权限 3:监控项　相关权限 4:树状节点 相关权限
    type = models.IntegerField()
    
    # 用户
    users = models.ManyToManyField(User) # 用户与权限多对多关联
    
# node ID 转换成 节点权限字符串
def nodeid2AuthStr(node_id,ptype):
    return "node_" + str(node_id) + '_' + ptype
    
# app_name 转换成对应的监控项权限字段  表示对此应用下的监控项有读或操作的权限
def app2AuthStr(app_name,ptype):
    return app_name + '_monitor_' + ptype  
     
#　语义监控　产品操作权限 
def product2AuthStr(product_id):
    return 'product_' +  str(product_id) + '_operate'
    
# 是否有某种类型的监控项权限    read 或 operate
def hasMonitorAuth(auth_set,ptype):
    keyword = "monitor_" + ptype
    for item in auth_set:
        if item.endswith(keyword):
            return True
    return False

# 可以对其监控项进行读操作的应用
def getAppListCanRead(auth_set):
    app_list = []
    service_list = AppService.objects.all();
    for service in service_list:
        if app2AuthStr(service.app_name,'read') in auth_set:
            app_list.append(service)
    
    return app_list

# 具有读权限的应用
def get_readable_app(request):
    auth_set = request.session["authority_set"]
    app_id_list = []
    service_list = AppService.objects.all();
    for service in service_list:
        if app2AuthStr(service.app_name,'read') in auth_set:
            app_id_list.append(service.id)
    return app_id_list
        
# -*- coding:utf-8 -*-
import re

from django.db import models
from appitem.models import AppService
from utils.constants import monitor_item_dict 
from authority.models import app2AuthStr
# 根据页面传递的类型和参数值生成nagios可识别的字符串
def generate_threshold(threshold_type,t,t1,t2):
    if threshold_type=='1':
        return '~:' + t
    elif threshold_type=='2':
        return t + ':'
    elif threshold_type=='3':
        return '@'+ t1 + ':' + t2
    else:
        return t1 + ':' + t2
        
# 根据ｎａｇｉｏｓ可识别的字符串，生成一个元组(threshold_type,t,t1,t2)
# 如果其中一个值不存在，则返回None
# threshold_type 如下:
# 1) x > t 
# 2) x < t   
# 3) t1 <= x <= t2  
# 4) x < t1 或　x > t2
def parse_threshold(threshold_str):
    t = None
    t1 = None
    t2 = None
    pattern_list = ['^~:([\d|\.]+)$','^([\d|\.]+):$','^@([\d|\.]+):([\d|\.]+)$','^([\d|\.]+):([\d|\.]+)$']
    for i in range(4):
        res = re.match(pattern_list[i],threshold_str)
        if res is not None:
            if i==0 or i==1:
                #print 'all:',res.groups()
                t = res.group(1)
            else:
                #print 'all:',res.groups()
                t1 = res.group(1)
                t2 = res.group(2)
            return (i+1,t,t1,t2)
        
    return None
    
# 监控项
class MonitorItem(models.Model):
    #重新定义表名
    class Meta:
        db_table = 'monitor_item'
    #类型   A/B
    monitor_type = models.CharField(max_length=1)
    #如果属于类型为A类用此值
    var_name = models.CharField(max_length=32,null=True)
    #如果属于B类用此公式
    formula = models.CharField(max_length=128,null=True)
    #警告阀值
    warning_threshold = models.CharField(max_length=32)
    #错误阀值
    critical_threshold = models.CharField(max_length=32)
    # 描述
    desc = models.CharField(max_length = 128)
    
    #外键  应用服务
    app = models.ForeignKey(AppService) # 多对一关联
    
    
        
    def __str__(self):
        return "{'desc':'%s','id':%s}" % (self.desc,self.id)
      
    def getMonitorType(self):
        return monitor_item_dict[self.monitor_type]
        
    def getAppName(self):
        return self.app.app_name
        
    def getContent(self):
        if self.monitor_type =='A':
            return self.var_name
        else:
            return self.formula
    
# 仅用于页面显示        
class MonitorItemExtend():
    def __init__(self):
        # id
        self.id =None
        # 描述
        self.desc = None
        # 所属应用
        self.app_name = None
        # 监控类型
        self.monitor_type = None
        # 变量或计算公式的内容
        self.content = None
        # 警告阀值
        self.warning_threshold = None
        # 错误阀值
        self.critical_threshold = None
        # 是否允许操作
        self.operate_permission = None

def monitorItem2Extend(auth_set,item_list):
    res_list = []
    for item in item_list:
        e = MonitorItemExtend()
        e.id = item.id
        e.desc = item.desc
        e.app_name = item.getAppName()
        e.monitor_type = item.getMonitorType()
        e.content = item.getContent()
        e.warning_threshold = item.warning_threshold
        e.critical_threshold = item.critical_threshold
        if app2AuthStr(item.getAppName(),"operate") in auth_set:
            e.operate_permission = True
        else:
            e.operate_permission = False
        res_list.append(e)
    return res_list
    
def monitorItem2Extend2(item_list):
    res_list = []
    for item in item_list:
        e = MonitorItemExtend()
        e.id = item.id
        e.desc = item.desc
        res_list.append(e)
    return res_list
    
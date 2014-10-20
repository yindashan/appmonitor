# -*- coding:utf-8 -*-
from django.db import models
import json

# our own code
from product.models import Product

# 服务组
class ServiceGroup(models.Model):
    #重新定义表名
    class Meta:
        db_table = 'service_group'
    #主键由Django生成
    # 产品
    product = models.ForeignKey(Product)
    # 名称
    name = models.CharField(max_length=32)
    # 备注
    comment = models.CharField(max_length=255)

# 某台机器提供的服务
class ServiceItem(models.Model):
    # 重新定义表名
    class Meta:
        db_table = 'service_item'
    # 主键由Django生成
    # 机房
    idc = models.IntegerField()
    # IP
    ip = models.CharField(max_length = 32)
    # port
    port = models.IntegerField()
    # 是否使用代理 0:否 1:是
    is_use_proxy = models.IntegerField()
    
    # 外键  服务组
    group = models.ForeignKey(ServiceGroup) # 多对一关联
    
# ServiceItem 扩展类
class ServiceItemExtend(object):
    def __init__(self,s):
        self.id = s.id
        self.idc = s.idc
        self.ip = s.ip
        self.port = s.port
        self.is_use_proxy = s.is_use_proxy
        dd = {'idc':s.idc,'ip':s.ip,'port':s.port,'is_use_proxy':s.is_use_proxy}
        self.json_data = json.dumps(dd)
        
    
    

# -*- coding:utf-8 -*-
from django.db import models

# stdandard library
import json


# our own code
from servicegroup.models import ServiceGroup
from product.models import Product

# 判断规则
class JudgeRule(models.Model):
    # 重新定义表名
    class Meta:
        db_table = 'judge_rule'
    # 主键由Django生成
    # 规则名称
    name = models.CharField(max_length=32)
    # 备注
    comment = models.CharField(max_length=255)
    # 对于规则的简单描述
    simple_desc = models.CharField(max_length=64)
    
# 测试集
class CaseSet(models.Model):
    # 重新定义表名
    class Meta:
        db_table = 'case_set'
    # 主键由Django生成
    # 产品
    product = models.ForeignKey(Product)
    # 名称
    name = models.CharField(max_length=32)
    # 备注
    comment = models.CharField(max_length=255)
    
    # 多对多
    service_groups = models.ManyToManyField(ServiceGroup) # 测试集和服务集群　多对多的关系
    
# 测试用例
class Case(models.Model):
    # 重新定义表名
    class Meta:
        db_table = 'test_case'
    # 主键由Django生成
    # URL
    url = models.TextField()
    # 备注
    comment = models.CharField(max_length=255)
    # 附加参数(以json字符串的形式存储)
    params = models.TextField()
    
    # 外键
    # 规则 多对一关联
    rule = models.ForeignKey(JudgeRule)
    # 测试集
    case_set = models.ForeignKey(CaseSet)
    
# Case 扩展类
class CaseExtend(object):
    def __init__(self,s):
        self.id = s.id
        self.url = s.url
        self.comment = s.comment
        self.params = s.params
        self.rule = s.rule
        dd = {'url':s.url, 'comment':s.comment, 'rule_id':s.rule.id, 'params':s.params}
        self.json_data = json.dumps(dd)
        

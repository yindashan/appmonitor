# -*- coding:utf-8 -*-
from django.db import models

class Chart(models.Model):
    # 重新定义表名
    class Meta:
        db_table = 'show_chart'
    # 主键由Django生成
    # 监控项id
    monitor_item_id = models.IntegerField(max_length=65) 
    # 应用所在ip
    host_ip = models.CharField(max_length=20, blank=True)
    # 展示类型,'1'4小时，'2'25小时，'3'一个月。'4'一年
    show_type = models.IntegerField(default=1)
    # 应用项主键
    app_id = models.IntegerField()
    # 应用名称 
    app_name = models.CharField(max_length=64)
    # 默认为有效
    status = models.IntegerField(default=1)
    app_id = models.IntegerField(max_length=10)
        
    def __str__(self):
        return str(self.monitor_item_id) + ' ' + self.host_ip
   
#仅用于方便的向页面传递参数
class ChartExtend(object):
    def __init__(self):
        self.id = None
        self.host_ip = None
        self.app_name = None
        self.monitor_item_id = None
        self.show_type = None
        self.desc = None
        #警告阀值
        self.warning_type = None;
        self.warning = None;
        self.warning_min = None;
        self.warning_max = None;
        #错误阀值
        self.critical_type = None;
        self.critical = None;
        self.critical_min = None;
        self.critical_max = None;
    def __str__(self):
        return str(self.app_name) + '_' + self.host_ip + '_' + self.desc
    
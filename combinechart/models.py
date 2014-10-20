# -*- coding:utf-8 -*-
from django.db import models
from showchart.models import Chart
from appitem.models import AppService
from utils.constants import combine_type_dict

# 联合图 
class CombineChart(models.Model):
    # 重新定义表名
    class Meta:
        db_table = 'combine_chart'
    # 主键由Django生成
    # 描述
    desc = models.CharField(max_length=255)
    # 1:曲线图 2:饼图
    type = models.IntegerField()
    
    #外键  应用服务
    app = models.ForeignKey(AppService) # 多对一关联
    
    charts = models.ManyToManyField(Chart) # 联合图和单数据源图多对多关联
    
class CombineChartExtend(object):
    def __init__(self):
        # 主键
        self.id = None
        # 描述
        self.desc = None
        # 类型
        self.type_str = None
        # 应用名称
        self.app_name = None
        # 应用描述
        self.app_desc = None

    
class CombineChartExtend2(object):
    def __init__(self):
        # canvas 的id
        self.canvas_id = None
        # 类型 饼图、曲线图、柱状图
        self.chart_type = None
        # 显示时间类型  4小时 1天 1月 1年
        self.show_type = None
        # 图表标题
        self.desc = None
        # 数据源id
        self.chart_ids = None
        # key 描述
        self.keys_desc = None
        
            
def getCombineChartExtendList():
    charts = CombineChart.objects.order_by('-id')
    return combine2Extend(charts)
    
def getCombineChartExtend(combine_id):
    chart = CombineChart.objects.get(id=combine_id)
    item = CombineChartExtend()
    item.id = chart.id
    item.desc = chart.desc
    item.type_str = combine_type_dict[chart.type]
    item.app_name = chart.app.app_name
    item.app_desc = chart.app.desc
    return item
    
def combine2Extend(charts):
    item_list = []
    for chart in charts:
        item = CombineChartExtend()
        item.id = chart.id
        item.desc = chart.desc
        item.type_str = combine_type_dict[chart.type]
        item.app_name = chart.app.app_name
        item.app_desc = chart.app.desc
        item_list.append(item)
    return item_list
    

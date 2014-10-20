# -*- coding:utf-8 -*-
from django.db import models
from django.db import connection

#our own code
from utils.utils import listToStr
from authority.models import nodeid2AuthStr,Permission
from utils.constants import show_type_dict
from appitem.models import AppService
from monitoritem.models import MonitorItem
from combinechart.models import CombineChart,CombineChartExtend2
from showchart.models import Chart,ChartExtend
from monitoritem.models import parse_threshold

        
#组织结构节点表
#+----+--------------+-----------+-------+
#| id | text         | parent_id | level |
#+----+--------------+-----------+-------+
#|  1 | 高德软件       |       -1 |     1 |
#+----+--------------+-----------+-------+
# 此节点作为展示的根节点
class ShowNode(models.Model):
    class Meta:
        db_table = "show_node"
    # 主键由Django生成
    # 节点显示文本
    text = models.CharField(max_length=64)
    # 父节点id
    parent_id = models.IntegerField()
    # 在树中的层级
    level = models.IntegerField()
    
    # 与联合表的关联关系
    combineCharts = models.ManyToManyField(CombineChart) # 节点与联合图的关联关系
    
    def __unicode__(self):
        return str(self.id) + ' ' + self.text

class NodeChartRelation(models.Model):
    class Meta:
        db_table = "node_chart_relation"
    #主键由Django生成  
    #show_node 表主键　代表　视图上的一个节点 
    show_node_id = models.IntegerField()
    #show_chart 表主键　代表 关于某个监控项的一张图
    show_chart_id = models.IntegerField()
     
# 提取树形结构,并返回以node_id 为根的树形结构对应的字典
# 加入权限控制  auth_set--权限集合 pnode_permission---父节点是有操作权限　control_level---权限控制层级
# 如果节点的层级大于control_level,则使用父节点的权限
def tree_structure(node_id,auth_set,pnode_permission,control_level):
    root_node = ShowNode.objects.get(id=node_id)
    if (root_node.level <=control_level) and (nodeid2AuthStr(node_id,'read') not in auth_set) :
        return None
        
    dd = {}
    #获取子树的根节点
    dd["id"] = root_node.id
    dd["text"] = root_node.text
    attributes = {}
    # 小于等于权限控制级别时检查节点权限，大于时，使用父节点的权限
    if root_node.level <= control_level:
        if nodeid2AuthStr(node_id,'operate') in auth_set:
            attributes["operate_permission"] = True
        else:
            attributes["operate_permission"] = False
    else:
        attributes["operate_permission"] = pnode_permission
        
    dd["attributes"] = attributes

    #判断其是否由子节点
    node_list = ShowNode.objects.filter(parent_id=node_id).order_by('text')
    child_list = []
    if node_list:
        for item in node_list:
                item_struct = tree_structure(item.id,auth_set,attributes["operate_permission"],control_level)
                if item_struct:
                    child_list.append(item_struct)
        if child_list:
            dd["state"] = "closed"   
            dd["children"] = child_list
        
    return dd;
    
#  *******************原始函数 请勿删除*****************   
##　提取树形结构,并返回以node_id 为根的树形结构对应的字典
#def tree_structure(node_id):
#    dd = {}
#    #获取子树的根节点
#    root_node = ShowNode.objects.get(id=node_id)
#    dd["id"] = root_node.id
#    dd["text"] = root_node.text
#    
#    #判断其是否由子节点
#    node_list = ShowNode.objects.filter(parent_id=node_id)
#    child_list = []
#    if len(node_list) > 0:
#        for item in node_list:
#            child_list.append(tree_structure(item.id))
#        dd["state"] = "closed"   
#        dd["children"] = child_list
#        
#    return dd;

# 用于配置读写权限
def right_tree_struct(node_id,control_level,purpose,auth_set):
    dd = {}
    auth_str = nodeid2AuthStr(node_id,purpose)
    #获取子树的根节点
    node = ShowNode.objects.get(id=node_id)
    dd["id"] = node.id
    dd["text"] = node.text
    
    permission_id = Permission.objects.get(codename=auth_str).id
    dd["attributes"] = {"permission_id":permission_id}
        
    if node.level < control_level:
        #判断其是否由子节点
        node_list = ShowNode.objects.filter(parent_id=node_id).order_by('text')
        child_list = []
        if node_list:
            for item in node_list:
                child_list.append(right_tree_struct(item.id,control_level,purpose,auth_set))
            dd["state"] = "closed"   
            dd["children"] = child_list
            
    # 复选框是否被选中
    if auth_str in auth_set:
        if node.level == control_level:
            dd["checked"] = True
        elif (node.level < control_level) and ("children" not in dd):
            dd["checked"] = True

    return dd
    
# 删除树中的节点,注意此节点可能有子节点    
def delete_node(node_id):
    # 遍历以此节点为根的子树
    id_list = []
    queue = [node_id]  
    #　广度优先遍历
    while len(queue) > 0 :
        # 访问次节点
        nid = queue.pop(0);
        id_list.append(nid);
        #判断其是否由子节点
        node_list = ShowNode.objects.filter(parent_id=nid)
        if node_list:
            for item in node_list:
                queue.append(item.id)
    # 执行删除操作
    ids = listToStr(id_list)
    
    # 删除与单数据源图表的关联关系        node_chart_relation表
    NodeChartRelation.objects.extra(where =['show_node_id IN (' + ids + ')']).delete()
    # 删除show_node_combineCharts表中的关联记录
    #使用基础函数访问数据库
    cursor = connection.cursor()
    sql = "delete from show_node_combineCharts where shownode_id in (" + ids + ")"
    cursor.execute(sql)
    # 删除show_node表中的记录
    ShowNode.objects.extra(where =['id IN (' + ids + ')']).delete()
    
    
        
# 增加子节点
def append_node(parent_id,text,control_level,id_array_str,combine_ids_str):
    parent_node = ShowNode.objects.get(id=parent_id)
    node = ShowNode();
    node.text = text;
    node.parent_id = parent_id;
    node.level = parent_node.level + 1
    node.save();
    
    # 配置关联关系
    # 单数据源图表
    if id_array_str:
        id_set = set(id_array_str.split(','))
        for item in id_set:
            relation = NodeChartRelation()
            relation.show_node_id = node.id
            relation.show_chart_id = int(item)
            relation.save();
    # 多数据源图表
    if combine_ids_str:
        id_set = set(combine_ids_str.split(','))
        for item in id_set:
            node.combineCharts.add(item)
    
    # 加入权限记录
    if node.level <= control_level:
        Permission(codename=nodeid2AuthStr(node.id,"read"),type=4).save()
        Permission(codename=nodeid2AuthStr(node.id,"operate"),type=4).save()
        
    return node;

# 更新节点的显示文字
def update_node(node_id,text,id_array_str,combine_ids_str):
    node = ShowNode.objects.get(id=node_id)
    node.text = text
    node.save();
    
    # 删除此节点与图表的已有关联关系
    NodeChartRelation.objects.filter(show_node_id=node_id).delete();
    # 配置关联关系
    if id_array_str:
        #id_set = set(id_array_str.split(','))
        id_list = id_array_str.split(',')
        for item in id_list:
            relation = NodeChartRelation()
            relation.show_node_id = node_id
            relation.show_chart_id = int(item)
            relation.save();
            
    # 删除此节点与联合图表的已有关联关系
    node.combineCharts.clear()
    # 多数据源图表
    if combine_ids_str:
        #id_set = set(combine_ids_str.split(','))
        id_list = combine_ids_str.split(',')
        for item in id_list:
            node.combineCharts.add(item)

#仅用于方便的向页面传递参数
class ShowChartExtend(object):
    def __init__(self):
        self.app_desc = None
        self.host_ip = None
        self.monitor_id = None
        self.monitor_desc = None
        self.show_type = None
        self.show_chart_id= None

# 按添加顺序返回数据源记录列表　　show_chart
def getDSBySort(combine_id):
    # 获取联合图关联的数据源信息
    cursor = connection.cursor()
    sql = "select c.id,c.monitor_item_id,c.show_type,c.app_id,c.host_ip,c.app_name from combine_chart_charts r,show_chart c where r.chart_id = c.id and c.status =1 and r.combinechart_id = %s order by r.id" 
    param = (combine_id)
    cursor.execute(sql, param)
    res = cursor.fetchall()
    charts = []
    for item in res:
        chart = Chart()
        chart.id = item[0]
        chart.monitor_item_id=item[1]
        chart.show_type = item[2]
        chart.app_id = item[3]
        chart.host_ip = item[4]
        chart.app_name = item[5]
        charts.append(chart)
    return charts


# 获取组合表的关联关系
def getCombineRealtion(combinechart):
    chart_list = []
    
    charts = getDSBySort(combinechart.id)
    
    for item in charts:
        chart = ShowChartExtend()
        chart.app_desc = AppService.objects.get(id = item.app_id).desc
        chart.host_ip = item.host_ip
        chart.monitor_id = item.monitor_item_id
        chart.monitor_desc = MonitorItem.objects.get(id= item.monitor_item_id).desc
        chart.show_type = show_type_dict[item.show_type]
        chart.show_chart_id = item.id
        chart_list.append(chart)
    return chart_list
    


# 用于页面产生图表        
def getChartlist(node_id):
    chart_list = []
    #使用基础函数访问数据库
    cursor = connection.cursor()
    sql = """select c.id,c.host_ip,c.app_name,c.monitor_item_id,c.show_type,m.desc,m.warning_threshold,m.critical_threshold from node_chart_relation r,monitor_item m, show_chart c 
    where r.show_node_id = %s and r.show_chart_id = c.id and m.id = c.monitor_item_id and c.status = 1 order by r.id;""" 
    param = (node_id)
    cursor.execute(sql, param)
    res = cursor.fetchall()
    #print '---------1---------',len(res)
    for item in res:
        chart = ChartExtend()
        chart.id = item[0]
        chart.host_ip = item[1]
        chart.app_name = item[2]
        chart.monitor_item_id = item[3]
        chart.show_type = item[4]
        chart.desc = item[5]
        
        #警告阀值
        warning_tuple = parse_threshold(item[6])
        chart.warning_type = warning_tuple[0]
        chart.warning = warning_tuple[1]
        chart.warning_min = warning_tuple[2]
        chart.warning_max = warning_tuple[3]
        #错误阀值
        critical_tuple = parse_threshold(item[7])
        chart.critical_type = critical_tuple[0]
        chart.critical = critical_tuple[1]
        chart.critical_min = critical_tuple[2]
        chart.critical_max = critical_tuple[3]
        chart_list.append(chart);
    #print '---------2---------',len(chart_list)
    return chart_list

# 节点对应联合图列表 按照关联表的id 升序
def getCombineChartBySort(node_id):
    #使用基础函数访问数据库
    cursor = connection.cursor()
    sql = "select c.id,c.desc,c.type,c.app_id from show_node_combineCharts r,combine_chart c where c.id = r.combinechart_id and r.shownode_id = %s order by r.id"   
    param = (node_id)
    cursor.execute(sql, param)
    res = cursor.fetchall()
    combineCharts = []
    for item in res:
        temp = CombineChart()
        temp.id = item[0]
        temp.desc = item[1]
        temp.type = item[2]
        temp.app_id = item[3]
        combineCharts.append(temp)
    return combineCharts


# 用于页面产生图表    联合图      
def getCombineChartlist(node_id):   

    combineCharts = getCombineChartBySort(node_id)
    
    # 组合图
    res_list = []
    for item in combineCharts:
        temp = CombineChartExtend2()
        temp.canvas_id = 'combine_' + str(item.id)
        temp.chart_type = item.type
        temp.desc = item.desc

        charts = getDSBySort(item.id)
        
        # show_type 4小时 1天 1月 1年
        if charts:
            temp.show_type = charts[0].show_type
        else:
            temp.show_type = 1
        chart_ids = ''
        keys_desc = ''
        for i in range(len(charts)):
            if i > 0:
                chart_ids +=','
                keys_desc +=','
            chart_ids += str(charts[i].id)
            keys_desc += MonitorItem.objects.get(id = charts[i].monitor_item_id).desc
        temp.chart_ids = chart_ids
        temp.keys_desc = keys_desc
        res_list.append(temp)
    return res_list

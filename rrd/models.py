# -*- coding:utf-8 -*-
from common.models import BusinessException  
import xml.etree.ElementTree as ET  
import time
import rrdtool 

        
#解析xml文件获取 dsname 和 ds 的对应关系
# <DATASOURCE> <DS></DS> <LABEL></LABEL> </DATASOURCE>   其中dsname 对应标签 LABEL,ds 对应标签 DS
def parse_cdp_xml(path,dsname):
    tree = ET.parse(path)
    root = tree.getroot()
    for element in root.findall('DATASOURCE'):
        if element.find('LABEL').text == dsname:
            return element.find('DS').text
    raise BusinessException(501)
    
#从rrd文件中提取cdp数据   CDP（consolidated data point）
#参数说明:
#    path --->rrd文件的路径
#    ds   --->rrd文件中监控项的名称
#    start--->开始时间
#    end  --->结束时间
#    resolution ----> 为时间间隔 
def fetch_rrd(path,ds,start,end,resolution):
        res = rrdtool.fetch(str(path),'AVERAGE','--resolution',str(resolution),'--start',str(start),'--end',str(end))
        # (start_time,end_time,resolution)
        start_time = res[0][0]
        #end_time = res[0][1]
        step = res[0][2]
        # ('ds1','ds2'... ...)
        index = -1
        for i in range(len(res[1])):
            if ds == res[1][i]:
                index = i
                break;
        if(index == -1):
            return BusinessException(101)
        # 开始取数据
        cdp_list = []
        for item in res[2]:
            temp = {}
            temp['time']= start_time
            temp['value']=item[index]
            cdp_list.append(temp)
            start_time +=step
        return cdp_list
        
            
            
        
    
    
    
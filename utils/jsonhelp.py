# -*- coding:utf-8 -*-

# 用户自定义类    
def obj2dict(obj):
    dd = {}
    # 展开它的属性
    for m in dir(obj):
        #print m
        if m[0] != "_" and not callable(m):
            value = getattr(obj,m)
            if isinstance(value,list) or isinstance(value,set):       # list  
                value = list2json(value)
            elif value == None or isinstance(value,int) or isinstance(value,long) or  \
            isinstance(value,str) or isinstance(value,unicode):  # int or str or long or unicode      
                pass
            elif isinstance(value,dict):     # dict
                value = dict2json(value)
            else:       # other class
                #print type(value)
                value = obj2dict(value)
                
            dd[m] = value     
    return dd
    
def list2json(ll):
    res_list = []
    for item in ll:
        value = complexObj2json(item)      
        res_list.append(value)  
    return res_list 
    
def dict2json(dd):
    res = {}
    for item in dd:
        res[item] = complexObj2json(dd[item])
    return res
    
# complex obj to json
# 复杂对象转换json对象 (dict、list)
def complexObj2json(obj):
    # list
    if isinstance(obj,list):
        return list2json(obj)
    # dict
    elif isinstance(obj,dict):
        return dict2json(obj)
    # 基本类型
    elif obj == None or isinstance(obj,int) or isinstance(obj,long) or  \
        isinstance(obj,str) or isinstance(obj,unicode):
        return obj
    # 用户自定义的类
    else:
        return obj2dict(obj)

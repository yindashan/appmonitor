# -*- coding:utf-8 -*-
from django.db import models

# 针对某个测试集的任务
class Task(models.Model):
    class Meta:
        db_table = 'check_task'
    # 主键由Django生成
    # 产品
    product = models.CharField(max_length=32)
    # 测试集ID
    set_id = models.IntegerField()
    # 0:初始 1:处理中 2:执行完成
    status = models.IntegerField()
    # 任务说明(测试集备注)
    comment = models.CharField(max_length=255)
    # 任务创建时间
    create_time = models.DateTimeField()
    # 任务执行时间
    execute_time = models.DateTimeField()
    # 是否通过 0:不通过 1:通过
    is_pass = models.IntegerField()


# 某个测试用例的某次检查结果
# 有类似快照的行为，保存测试的URL, 规则, 附加参数 
class CheckResult(models.Model):
    # 重新定义表名
    class Meta:
        db_table = 'check_result'
    # 主键由Django生成
    # 执行时间
    execute_time = models.DateTimeField()
    # 测试用例ID
    case_id = models.IntegerField()
    # URL
    url = models.TextField()
    # 测试用例备注
    case_comment = models.CharField(max_length=255)
    # 是否通过 0:不通过 1:通过
    is_pass = models.IntegerField()
    # 备注信息,详细阐述失败的原因,内容比较多
    comment = models.TextField()
    # 附加参数  以JSON字符串保存
    params = models.TextField()
    # 规则(规则简单描述)
    rule = models.CharField(max_length=64)
    
    #外键  应用服务
    task = models.ForeignKey(Task) # 多对一关联
    
    
    
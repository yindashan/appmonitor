# -*- coding:utf-8 -*-
from django.db import models

#应用服务
class AppService(models.Model):
    #重新定义表名
    class Meta:
        db_table = 'app_service'
    #主键由Django生成
    #应用名称
    app_name = models.CharField(max_length=64,unique = True)
    #关于此应用的描述
    desc = models.CharField(max_length=128)
    #应用所在服务器的IP地址列表，以逗号分隔  如：192.168.1.122,10.2.161.51,192.168.1.110
    ip_list = models.TextField()
    
    # 邮件列表
    email_list = models.CharField(max_length = 255)
    # 手机列表
    mobile_list = models.CharField(max_length = 255)
    # 报警类型,0代表不报警,1代表不报警
    alarmtype = models.IntegerField(default=0)
    
    # 检查时间间隔 (单位:分钟)
    check_interval = models.IntegerField(default=5)
    # 最大检查次数 决定应用是否达到 hard state (连续几次检查都超过阀值才会触发报警)
    max_check_attempts = models.IntegerField(default=2)
        
    def __unicode__(self):
        return str(self.id) + ' ' + self.desc     
        
        
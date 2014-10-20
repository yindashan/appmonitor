# -*- coding:utf-8 -*-
from django.db import models
from authority.models import product2AuthStr

# 产品
class Product(models.Model):
    # 重新定义表名
    class Meta:
        db_table = 'product'
    # 主键由Django生成
    # 产品名称
    product_name = models.CharField(max_length=32)
    
# 获取用户可用的产品ID集合
def get_usable_product(request):
    auth_set = request.session["authority_set"]
    product_id_list = []
    product_list = Product.objects.all()
    for product in product_list:
        if product2AuthStr(product.id) in auth_set:
            product_id_list.append(product.id)
    return product_id_list
        
        
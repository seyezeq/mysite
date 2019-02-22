from django.contrib import admin

#导入数据库
from supermarket.models import Product
#注册数据类
@admin.register(Product)
#继承admin基类
class ProductAdmin(admin.ModelAdmin):
    #显示字段
    list_display =('id','name','price')
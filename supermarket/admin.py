from django.contrib import admin
from supermarket.models import Product,Permission,Node
from mysite.models import User
#注册数据类
@admin.register(Product)
#继承admin基类
class ProductAdmin(admin.ModelAdmin):
    #显示字段
    list_display =('id','name','price','count')
    #分页设置,系统默认一页100条
    list_per_page = 5
    #排序
    ordering = ('-id',)
    #设置可进入编辑的超链接
    list_display_links = ('name',)
    #设置直接在列表页修改
    list_editable = ['price']
    #设置搜索功能
    search_fields = ['name']
    # 定制右侧快速筛选，可以组合筛选
    list_filter = ('id','name')
  

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display =('id','username','password','gender','time')
    data_hierarchy = "time"

@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('id','name')

@admin.register(Permission)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('id','nid','gid')

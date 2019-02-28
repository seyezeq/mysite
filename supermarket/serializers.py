#导入序列化库
from rest_framework import serializers
#导入数据库类
from supermarket.models import Product
#定义序列化类
class ProductSerializers(serializers.ModelSerializer):
    #定义内置类  
    class Meta:
        #指定序列化的字段
        model = Product
        # fields = ('id','name','price','count')
        #取所有的字段
        fields = "__all__"
    
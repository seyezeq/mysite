#导包导入django数据库类
from django.db import models

#建立数据库类
class User(models.Model):
    #主键 通过参数声明主键
    id = models.IntegerField(primary_key=True)
    #用户名 字符串类型需要声明长度限制
    username = models.CharField(max_length=200)
    #密码
    password = models.CharField(max_length=100)
    #时间字段
    time = models.DateTimeField()
    #图片 
    img = models.CharField(max_length=200)


    #声明表名
    class Meta:
        #必须和数据库中的表名吻合
        db_table = "user"
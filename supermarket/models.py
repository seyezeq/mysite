#导包导入django数据库类
from django.db import models

#建立数据库类
class Product(models.Model):
    #主键 通过参数声明主键 Autofield是自动增长字段
    id = models.AutoField(primary_key=True)
    #商品名称 字符串类型需要声明长度限制
    name = models.CharField(max_length=200)
    #价格
    price = models.IntegerField()
    count = models.IntegerField()

    #声明表名
    class Meta:
        #必须和数据库中的表名吻合
        db_table = "product"
    def __str__(self):
        return self.name
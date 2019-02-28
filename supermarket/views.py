from django.shortcuts import render
#导包
from django.http import HttpResponse,HttpResponseRedirect
#导入类路由库
from django.views import View
#导入数据库类
from mysite.models import User
from supermarket.models import Product
#导入json
import json
#导入时间模块
import time
#导入django内置的密码库
from django.contrib.auth.hashers import make_password,check_password
#导入自定义过滤器方法
import mysite.templatetags.my_filter
#导入类装饰器库
from django.utils.decorators import method_decorator
#导入装饰器
from mysite.d7 import check_login
#导入分页器
from django.core.paginator import Paginator
#导入数据库连接方法
from django.db import connection
#导入绘图库
from PIL import ImageDraw
#导入绘图字体库
from PIL import ImageFont
#导入图片库
from PIL import Image
#导入io库
import io
#导入随机库
import random


#导入视图类
from rest_framework import viewsets
from .serializers import ProductSerializers
#定义类，属于rest专用类，专门定义json接口
class ProductViewsets(viewsets.ModelViewSet):
    #输出序列化类
    #定义sql
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


#定义用户详情页
class UserInfo(View):
    def get(self,request):
        username = request.COOKIES.get('username')
        #定义游标
        cursor = connection.cursor()
        cursor.execute("select c.name,c.id from user as a left join user2group as b on a.id = b.uid left join usergroup as c on b.gid = c.id where a.username='%s'" % username)
        #调用fetchone fetchall
        res = cursor.fetchall()

        #查询普通用户的所有账户
        cursor.execute("select c.username,c.id from usergroup as a left join user2group as b on a.id = b.gid left join user as c on b.uid = c.id where a.name='普通用户'")
        #调用fetchone fetchall
        res_1 = cursor.fetchall()
        cursor.close()
        return render(request,'supermarket/userinfo.html',locals())
class Password_update(View):
    def post(self,request):
        password = request.POST.get("password")
        password1 = request.POST.get("password1")
        user = request.COOKIES.get("username")
        password = make_password(password,'123')
        password1 = make_password(password1,'123')
        res = User.objects.filter(username=user).values('password')
        res =list(res)
        res = res[0]["password"]
        print(res,password)
        if res == password:
            User.objects.filter(username=user).update(password=password1)
            return HttpResponse("修改成功")
        else:
            return HttpResponse("密码不正确")


#定义随机颜色方法
def get_random_color():
    R = random.randrange(255)
    G = random.randrange(255)
    B = random.randrange(255)
    return (R,G,B)
#定义随机验证码
def test_captcha(request):
    #定义背景颜色
    bg_color = get_random_color()
    #定义画布大小 宽，高
    img_size = (150,80)
    #定义画笔 颜色种类,画布，背景颜色
    image = Image.new("RGB",img_size,bg_color)
    #定义画笔对象 图片对象,颜色类型
    draw = ImageDraw.Draw(image,'RGB')
    #定义随机字符
    source = '0123456789asdfghjkl'
    #定义四个字符
    #定义好容器，用来接收随机字符串
    code_str = ''
    for i in range(4):
        #获取随机颜色 字体颜色
        text_color = get_random_color()
        #获取随机字符串
        tmp_num = random.randrange(len(source))
        #获取字符集
        random_str = source[tmp_num]
        #将随机生成的字符串添加到容器中
        code_str += random_str
        #将字符画到画布上 坐标，字符串，字符串颜色，字体
        #导入系统真实字体,字号
        my_font = ImageFont.truetype("c:\\windows\\Fonts\\arial.ttf",20)
        draw.text((10+30*i,20),random_str,text_color,font=my_font)
    #使用io获取一个缓存区
    buf = io.BytesIO()
    #将图片保存到缓存区
    image.save(buf,'png')

    #将随机码存储到session中
    request.session['code'] = code_str

    #第二个参数声明头部信息
    return HttpResponse(buf.getvalue(),'image/png')

#导入django模块
from django.http import HttpResponse,HttpResponseRedirect
from datetime import datetime
from django.utils.timezone import make_aware
from mysite.my_models import *
from django.shortcuts import render
#序列化
import json
from mysite.models import *
from mysite import settings
import datetime
import os
from mysite.d3 import limit

from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image
import io


import random

def get_random_color():
    R = random.randrange(255)
    G = random.randrange(255)
    B = random.randrange(255)
    return (R, G, B)


def Check_Login(func):  #自定义登录验证装饰器
    def warpper(request,*args,**kwargs):
        is_login = request.session.get('username', False)
        if is_login:
            ret = func(request,*args,**kwargs)
            return ret
        else:
            return HttpResponseRedirect("/")
    return warpper


#定义视图方法
#@limit(seconds=3)
def tu(request):
    # 定义画布背景颜色
    bg_color = get_random_color()
    # 画布大小
    img_size = (130, 70)
    # 定义画布
    image = Image.new("RGB", img_size, bg_color)
    # 定义画笔
    draw = ImageDraw.Draw(image, "RGB")
    # 准备画布上的字符集
    source = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789"
    # 保存每次随机出来的字符
    code_str = ""
    for i in range(4):
        # 获取数字随机颜色
        text_color = get_random_color()
        # 获取随机数字 len
        tmp_num = random.randrange(len(source))
        # 获取随机字符 画布上的字符集
        random_str = source[tmp_num]
        # 将每次随机的字符保存（遍历） 随机四次
        code_str += random_str
        # 将字符画到画布上
        draw.text((10 + 30*i, 20), random_str, text_color, font=None)
    # 记录给哪个请求发了什么验证码
    request.session['code'] = code_str
    
    # 获得一个缓存区
    buf = io.BytesIO()
    # 将图片保存到缓存区
    image.save(buf, 'png')
    # 将缓存区的内容返回给前端 .getvalue 是把缓存区的所有数据读取
    return HttpResponse(buf.getvalue(), 'image/png')

def index(request):
    res = User.objects.filter().values()
    res = list(res)
    for item in res:
        item['time'] = str(item['time'])[0:19]

    user = User(username='123',password='123',time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    user.save()
    
    data = json.dumps(res,ensure_ascii=False)

    if request.method == 'POST':
        obj = request.FILES.get("img")
        print(obj)
        f = open(os.path.join(settings.UPLOAD_ROOT,'',obj.name),'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()

        return HttpResponse('ok')
    
    return render(request,'test.html')
    return HttpResponse(data)


def test123(request,p1):
    p1 = request.POST.get('name','未接到name')
    data = {'name':p1}
    data = json.dumps(data,ensure_ascii=False) #不转码
    return HttpResponse(data,content_type="application/json")
    #return HttpResponse(" 123 ")



#定义视图方法
def test(request):

    #接收通过get方式传过来的参数,第二个参数用来判断，如果没有该值，赋一个值
    id = request.GET.get('id','未接到参数')
    print(id)

    return HttpResponseRedirect('/123')

    return HttpResponse(" 这里是test 参数是 " + id )


#定义视图方法
def test_re(request,p1,p2):
    #返回一个字符串
    return HttpResponse(" 这里是正则路由 " + str(p1) + str(p2) )
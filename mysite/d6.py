#导包
from django.http import HttpResponse,HttpResponseRedirect
#模板模块
from django.shortcuts import render
#导入数据模型类
from mysite.models import User

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

#导入装饰器
from mysite.d7 import check_login


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



#定义视图方法
def index(request):

    #判断请求方式
    if request.method == 'POST':
        #接收参数
        username = request.POST.get('username','未收到用户名')
        password = request.POST.get('password','未收到密码')

        #判断用户名或者密码是否正确 返回数量
        res = User.objects.filter(username=username,password=password).count()

        #测试验证码逻辑
        #return HttpResponse(request.session.get('code','未拿到session'))

        #判断验证码是否输入正确
        #接收验证码
        code = request.POST.get("code","未收到验证码")
        if code != request.session['code']:
            return HttpResponse("您输入的验证码有误，请重新输入")

        if res == 0:
            return HttpResponse("您的用户名或者密码错误")
        else:
            #登录成功就重定向到详情页
            #先存入session
            request.session['username'] = username
            return HttpResponseRedirect('/d6_info')
    return render(request,'d6_login.html')


#定义详情页视图
@check_login
def d6_info(request):

    #获取session
    username = request.session.get('username','未登录')

    #显示用户详情页具体用户信息
    res = User.objects.get(username=username)

    #判断是否登录
    # if username == '未登录':
    #     #跳转登录页面
    #     return HttpResponseRedirect('/')

    return render(request,'d6_info.html',locals())


#定义注销视图方法
def d6_logout(request):
    #删除session
    del request.session['username']
    #跳转到登录页面
    return HttpResponseRedirect("/")
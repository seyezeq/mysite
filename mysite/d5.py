#导包
from django.http import HttpResponse,HttpResponseRedirect
#导入数据库模型
from mysite.models import *
#导入模板库
from django.shortcuts import render
#导入connection模块用来修改或者删除操作
from django.db import connection
#导入json模块
import json
#导入时间模块
from datetime import datetime
#导入配置文件
from mysite import settings
#导入os模块
import os



#建立视图方法
def index(request):

    #执行原生sql语句 raw方法内，可以写任意sql语句
    res = User.objects.raw(' select * from user limit 1 ')
    #对raw对象进行格式转化 需要注意：使用raw原生sql，返回的结果集和传统orm方法有区别
    res = list(res)
    #print(res)
    #使用raw方法只能用来查询

    #定义游标对象用来执行sql语句
    # with connection.cursor() as c:
    #     c.execute(" update user set password = '66666' where id = 10 ")

    #进行删除操作
    # with connection.cursor() as c:
    #     c.execute(" delete from user where id = 19 ")

    #入库操作 时间类型
    #实例化对象 格式化时间
    user = User(username='测试时间',password='123',time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #调用save方法
    user.save()


    

    return render(request,'d5_index.html',locals())


#定义接口方法
def test_json(request):
    #定义数据
    data = [{'name':'你好','age':30},{'name':'rose','age':20},{'name':'anne','age':18}]
    #读取动态数据
    #使用values()方法可以自动将结果集转换成可用模式
    data = User.objects.all().values()
    data = list(data)
    #遍历强转
    for item in data:
        #使用[开始:截取多少位] 来切字符串
        item['time'] = str(item['time'])[0:19]
    #将数据转换成json格式
    #dump和dumps区别就是 dump用于文件操作 dumps用于字符串操作
    #使用第二个参数，将ascii码转义关闭
    data = json.dumps(data,ensure_ascii=False)
    return HttpResponse(data)


#定义注册逻辑
def test_register(request):

    #判断请求方式
    if request.method == 'POST':
        #接收参数
        username = request.POST.get("username","未接到用户名")
        password = request.POST.get("password","未接到密码")

        #接收文件，以对象的形式
        img = request.FILES.get("img")
        #文件名称是name属性

        #建立文件流对象
        f = open(os.path.join(settings.UPLOAD_ROOT,'',img.name),'wb')

        #写文件 遍历图片文件流
        for chunk in img.chunks():
            f.write(chunk)
        #关闭文件流
        f.close()

        #入库操作
        user = User(username=username,password=password,img=img.name)
        user.save()

        return HttpResponse('注册成功') 

    return render(request,'d5_register.html')

#用户详情页
def user_info(request):
    #读取用户信息
    res = User.objects.get(id=46)

    return render(request,'d5_userinfo.html',locals())
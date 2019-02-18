#导包
from django.http import HttpResponse,HttpResponseRedirect
#导入模板模块
from django.shortcuts import render
#导入json库
import json

import time

#定义视图方法
def index(request):

    return render(request,'d7_index.html')


#定义json接口
def d7_json(request,username):

    #time.sleep(10)

    #接收post请求参数
    username = request.POST.get("name","未收到post参数")


    #定义返回对象
    data = {'name':username}
    #强转数据类型
    data = json.dumps(data,ensure_ascii=False)
    #返回json数据 第二个参数通知浏览器，这是json数据
    return HttpResponse(data,content_type="application/json")


#定义一个验证登录的装饰器
def check_login(func):
    def warpper(request,*args,**kwargs):
        #is_login = request.session.get("username",False)
        is_login = request.COOKIES.get("username",False)
        if is_login:
            ret = func(request,*args,**kwargs)
            return ret
        else:
            return HttpResponseRedirect("/supermarket")
    return warpper


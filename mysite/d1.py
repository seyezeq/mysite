#导入django模块 重定向依赖于 HttpResponseRedirect
from django.http import HttpResponse,HttpResponseRedirect
#导入时间模块
from datetime import datetime
#导入django内置的时间转换模块
from django.utils.timezone import make_aware
from django.shortcuts import render



#定义视图方法
def index(request):
    return render(request,"index.html",{"k1": "v1", "k2":[11, 22, 33],"k3":{"nid":12,"name":"aaa"},'num':100})


#定义跳转页面
def re_url(request):

    #进行重定向操作
    return HttpResponseRedirect('/test-123-')
    return HttpResponse(" 跳转123 ")




#定义视图方法
def test(request):

    #接收通过get方式传过来的参数,第二个参数用来判断，如果没有该值，赋一个值
    id = request.GET.get('id','未接到参数')
    #通过POST属性来接收post过来的参数
    id = request.POST.get('id','未接收到post参数')
    print(id)

    return HttpResponse(" 这里是test 参数是 " + id )


#定义视图方法
def test_re(request,p1,p2):
    #返回一个字符串
    return HttpResponse(" 这里是正则路由 " + str(p1) + str(p2) )


#定义设置cookie(存储)
def save_cookie(request):
    #定义回应
    response = HttpResponse("存储cookie ok")
    #定义过期时间
    expires = datetime(year=2019,month=11,day=20,hour=15,minute=5,second=0)
    #转储为django内置时间
    expires = make_aware(expires)
    #进行存储动作
    response.set_cookie("username","jack",expires=expires)
    #将回应对象返回
    return response

#定义获取cookie（取）
def get_cookie(request):
    #定义变量获取cookies属性
    cookies = request.COOKIES
    #从cookies通过key获取value
    username = cookies.get("username","未拿到用户名")
    #将用户名返回
    return HttpResponse(username)


#定义删除cookie方法
def del_cookie(request):
    #定义response对象
    response = HttpResponse("删除cookie成功")
    #调用delete_cookie()方法来删除cookie
    response.delete_cookie("username")
    #返回response
    return response

def page_not_found(request,**kwargs):
    return HttpResponse("404")

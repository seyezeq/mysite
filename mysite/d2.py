#导包
from django.http import HttpResponse,HttpResponseRedirect
#导入模板解析库
from django.shortcuts import render
#导入日期模块
import datetime


#定义视图方法
def page_not_found(request,**kwargs):
    #解析404模板
    return render(request,'d2_404.html')
    #return HttpResponse("您的页面找不到啦")

#定义视图方法
def test_email(request,p1,p2,p3):
    #定义回应
    response = HttpResponse("存储成功")
    #第三个参数也可以传max_age,单位是秒
    response.set_cookie("email",p1,max_age=10)
    #返回回应
    return response


def test(request):
    ip = request.POST.get('ip','未接收到ip')
    port = request.POST.get('port','未接收到port')

    return HttpResponseRedirect('/')
    return HttpResponse(str(ip) + ":" + str(port) )



#定义首页方法
def index(request):
    #调用render方法来解析模板，第一个参数是request,第二个参数是模板文件名,第三个参数传值
    #定义变量，输出到模板
    
    test_str = 'Hello World'
    test_int = 100
    test_list = ['牛奶','鲜花','咖啡','电视']
    test_dict = [{'name':'小明','age':18},{'name':'小红','age':15}]
    content = 'Hello,I am Jack How do u do?'
    dt = datetime.datetime.now()
    return render(request,'d2_index.html',{'test_str':test_str,'test_int':test_int,'test_list':test_list,'test_dict':test_dict,'content':content,'dt':dt})


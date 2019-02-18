#导包
from django.http import HttpResponse,HttpResponseRedirect
#导内置模板方法
from django.shortcuts import render
#导入时间模块
import time


#定义反扒装饰器,定义形参，一秒允许请求一次
def limit(seconds=1):
    #定义内部方法
    def rate_limit(func):
        def func_limit(request):
            #获取当前时间
            now = time.time()
            #获取首次来访时间
            request_time = request.session.get('req_time',0)
            #做减法
            in_time = int(now) - request_time
            #判断访问者在一秒内来了不止一次
            if in_time < seconds:
                #抛出异常 ,使用第二个参数来指定异常
                return HttpResponse('你是爬虫，不要来了',status=403)
            else:
                #来的时间点存储
                request.session['req_time'] = time.time()
                #让访问者继续访问
                ret = func(request)
                return ret
        return func_limit
    return rate_limit


#定义视图方法
@limit(seconds=10)
def index(request):
    test_str = 'templatetags'
    test_list = [1,2,3,4]
    test_int = 99
    test_b = '<b>你好</b>'

    print(request.session.get('str','未收到礼物'))

    #后台来编写table
    #定义表格的起始标签
    my_table = "<table>"
    #在循环内填充表格
    for item in test_list:
        #定义好一个类选择器
        my_class = ''
        #判断奇数还是偶数
        if item % 2 == 0:
            my_class = 'tr2'
        else:
            my_class = 'tr1'
        #将判断后的类选择器填入字符串
        my_table += "<tr class='%s'><td>%s</td></tr>" % (my_class,str(item))
    #补全标签
    my_table += "</table>"

    #使用locals()方法，可以将视图方法内所有的变量默认传参
    return render(request,'d3_index.html',locals())


#定义存储session
def save_session(request):
    #存储动作
    request.session['username'] = '你好'
    return HttpResponse("存储成功")


#定义取值方法
def get_session(request):
    #取值
    return HttpResponse(request.session.get('str','未取到'))


#定义删除session方法
def del_session(request):
    #删除动作
    del request.session['username']
    return HttpResponse("删除成功")
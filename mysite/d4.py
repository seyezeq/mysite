#导包
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden
#导入自定义的数据库模型
from mysite.models import User
#导内置模板方法
from django.shortcuts import render


#定义视图方法
def get_ip(request):
    #打印头部信息
    #print(request.META)
    #获取ip信息
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
    else:
        ip = request.META.get('REMOTE_ADDR')

    print("来访者的ip是"+str(ip))
    return HttpResponse("您的ip是"+str(ip))


#定义首页视图方法
def index(request):
    #入库操作（增）
    #建立实例
    #user = User(username='新用户',password='你好')
    #入库操作
    #user.save()

    #删除数据（删）
    #User.objects.filter(username='新用户').delete()


    #修改数据(改) 第一种方式
    #user = User.objects.get(id=9)
    #修改字段
    #user.username = '1234'
    #保存修改
    #user.save()

    #修改数据（改） 第二种方式
    #return HttpResponse('',status=403)
    
    #User.objects.filter(id=9).update(password='新密码')


    #查询全部数据 翻译为 select * from user; all()返回值是list
    res = User.objects.all()
    #print(res)

    #查询限定条件的数据 翻译为 select * from user where username = '新用户123' and逻辑使用多个参数传递
    res = User.objects.filter(username='新用户',password='你好')
    #print(res)

    #只取一条 翻译 select * from user where id = 1
    res_one = User.objects.get(id=1)
    #print(res_one)

    #排除条件  翻译为 select * from user where username != '新用户123'   <>
    res = User.objects.exclude(username='新用户')

    #定制字段显示 翻译为 select password from user where name = '新用户'
    res_s = User.objects.filter(username='新用户').values('password')

    #排序 翻译为 select * from user order by id asc  倒序使用 reverse()
    res = User.objects.filter(username='新用户').order_by("password").reverse()

    #去重 翻译为 select distinct(username) from user where username = '新用户'
    res_dis = User.objects.filter(username='新用户').values('username').distinct()
    #print(res_dis)

    #取数量 翻译为 select count(*) from user
    res_count = User.objects.filter(username='新用户').count()
    print(res_count)

    res_list = [{'name':'小王','score':100,'gender':'男'},{'name':'小宏','score':50,'gender':'女'}]


    return render(request,'d4_index.html',locals())

#定义捕获500的异常
def page_not_error(request,**kwargs):
    return HttpResponse("捕获500异常")

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


#定义添加购物车逻辑
class AddCart(View):
    #定义添加方法
    def post(self,request):
        #接收参数
        id = request.POST.get('id')
        #判断购物车是否存在
        cart_list = request.session.get('cartlist','no')
        #如果不存在就创建后添加
        if cart_list == 'no':
            clist = []
            clist.append(int(id))
            request.session['cartlist'] = clist
        else:
        #如果存在，就直接添加 强转数据类型
            request.session['cartlist'].append(int(id))


        return HttpResponse('添加成功')


#定义清空购物车功能
class ClearCart(View):
    #定义get方法
    def get(self,request):
        #直接进行清空操作
        #使用异常捕获来捕获可能出现的error
        try:
            del request.session['cartlist']
        except Exception as e:
            #将错误异常强转为string，方便后台打印查看
            print(str(e))
            pass
        return HttpResponse('清空购物车成功')


#定义购物车列表


class CartList(View):
    #定义列表方法
    def get(self,request):
        #读取session
        cartlist_old = request.session.get('cartlist',0)

        #使用orm in 操作 来实现单条语句查询
        #捕获异常
        try:
            cartlist = Product.objects.filter(id__in=cartlist_old)
        except Exception as e:
            cartlist = 0

        return render(request,'supermarket/cartlist.html',locals())



#定义注销功能
class Logout(View):
    #定义注销方法
    def get(self,request):
        #建立response对象
        response = HttpResponseRedirect("/supermarket/login")
        #删除cookie
        response.delete_cookie("username")
        return response


#定义商品删除操作
class ProDel(View):
    #定义删除方法
    def post(self,request):
        #接收参数
        id = request.POST.get('id')
        #删除操作
        Product.objects.filter(id=int(id)).delete()
        return HttpResponse("删除成功")


#定义商品编辑操作
class ProEdit(View):
    #定义编辑方法
    def post(self,request):
        #接收两个参数
        id = request.POST.get("id")
        price = request.POST.get("price")

        #进行修改操作
        Product.objects.filter(id=int(id)).update(price=int(price))

        return HttpResponse("修改成功")


#定义商品列表页视图
class ProList(View):
    #定义商品列表方法
    def get(self,request):
        #读取数据库
        res = Product.objects.all()
        #获取用户名
        username = request.COOKIES.get('username','未登录')
        #对用户名进行解码
        username = username.encode("ISO-8859-1").decode("utf-8")
        #解析模板
        return render(request,'supermarket/prolist.html',locals())



#定义登录逻辑
class Login(View):
    
    #定义登录方法
    def post(self,request):
        #time.sleep(5)
        #接收参数
        username = request.POST.get('username','未收到username')
        password = request.POST.get('password','未收到password')


        #对秘钥加密
        password_hash = make_password(password,'123')

        #利用check_password来比对密码
        #print(check_password(password,make_password(password,'123')))
        print(password_hash)       

        #判断用户名和密码
        res = User.objects.filter(username=username,password=password_hash).count()
        

        if res > 0:
            #登录成功的逻辑
            response = HttpResponse('登录成功')
            #对中文进行编码
            username = bytes(username,'utf-8').decode('ISO-8859-1')
            response.set_cookie("username",username,max_age=3600)
            response.set_cookie("password",password,max_age=3600)
            return response
        else:
            #登录失败的逻辑
            return HttpResponse('您的用户名或者密码错误')


#定义注册逻辑
class Reg(View):

    #定义注册接收方法
    def post(self,request):

        #time.sleep(5)

        #接收参数
        username = request.POST.get('username','未收到username')
        password = request.POST.get('password','未收到password')

        #入库逻辑
        #验证唯一性
        res = User.objects.filter(username=username).count()
        if res > 0:
            #强转为json数据
            data = json.dumps({'msg':'请您换一个用户名'},ensure_ascii=False)
            return HttpResponse(data,content_type='application/json')
        else:
            #进行入库
            #实例化一个对象
            #进行秘钥加密
            password = make_password(password,'123')
            user = User(username=username,password=password)
            #保存
            user.save()
            data = json.dumps({'msg':'恭喜您，注册成功'},ensure_ascii=False)
            return HttpResponse(data,content_type='application/json')


        

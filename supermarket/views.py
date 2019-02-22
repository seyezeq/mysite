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
#定义删除购物车逻辑
class DelCart(View):
    def post(self,request):
        id = request.POST.get('id')
        id = int(id)
        #获取购物车列表
        cartlist = request.session.get('cartlist')
       #过滤删掉的商品ID
        slist = filter(lambda x:x!=id,cartlist)
        slist = list(slist)
        #将过滤后的购物车赋值
        request.session['cartlist'] = slist
        return HttpResponse('删除成功')
#定义购物车列表
class CartList(View):
    #定义列表方法
    @method_decorator(check_login,name="get")
    def get(self,request):
        #读取session
        cartlist_old = request.session.get('cartlist',0)
        #使用orm in 操作 来实现单条语句查询
        #捕获异常
        try:
            cartlist = Product.objects.filter(id__in=cartlist_old)
        except Exception as e:
            cartlist = 0
        #定义title
        html_title="购物车列表"
        #j计算总价
        sum_price = 0
        #遍历商品列表
        for item in cartlist:
            #调用自定义过滤器方法来计算商品个数
            product_count = mysite.templatetags.my_filter.supermarket_count(item.id,cartlist_old)

            sum_price += (item.price*product_count)

        return render(request,'supermarket/cartlist.html',locals())
#定义单个修改购物车数量
class EditCart(View):
    def post(self,request):
        id = request.POST.get("id")
        type = request.POST.get("type")
        #获取购物车
        cartlist = request.session.get('cartlist')
        if type == "+":
            cartlist.append(int(id))
        else:
            cartlist.remove(int(id))
        request.session['cartlist'] = cartlist
        return HttpResponse('操作成功')
#批量修改购物车数量
class DoEditCart(View):
    def post(self,request):
        id = request.POST.get("id")
        count = request.POST.get("count")
        #读取库存
        # procount = Product.objects.filter(id=int(id)).values('count')
        # procount = procount[0]['count']
        procount = Product.objects.get(id=int(id))
        procount = procount.count
        if int(count) > procount:
            return HttpResponse("库存不足")
        #获取购物车
        carlist = request.session.get('cartlist')
        #清除更改购物车商品
        cartlist_new = filter(lambda x:x!=int(id),carlist)
        cartlist_new = list(cartlist_new)
        #将购买数量添加到购物车
        for n in range(int(count)):
            cartlist_new.append(int(id))
        #购物车重新赋值
        request.session['cartlist'] = cartlist_new
        return HttpResponse("ok")
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
        searchtitle = request.GET.get('searchtitle','')
        #清除字符串两边 的空格
        searchtitle = searchtitle.strip()
        res = Product.objects.filter(name__contains = searchtitle).order_by('-price','-count')
        #读取数据库
        # res = Product.objects.all()
        #建立分页器对象 ,第一个参数结果集，第二个每页的参数
        paginator = Paginator(res,3)
        #接收分页的参数
        page = request.GET.get('page',1)
        #将结果集按照分页逻辑切片
        res = paginator.get_page(page)
        page_list = [s for s in range(1,res.paginator.num_pages+1)]
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
#定义批量删除逻辑
class Group_Del(View):
    def post(self,request):
        ids = request.POST.get("ids")
        #使用eval方法来强转为list
        ids = eval('['+ids+"]")
        #删除操作
        Product.objects.filter(id__in=ids).delete()
        return HttpResponse("ok")

        

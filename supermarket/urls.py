#导包
from django.urls import path,re_path

#导入类视图模板模块
from django.views.generic import TemplateView

#导入类视图文件
from supermarket.views import *

#导入装饰器
from mysite.d7 import check_login   
from supermarket.user import Reg,Login,Logout
from supermarket.product import *
from supermarket.cart import *
#导入路由库
from rest_framework.routers import DefaultRouter
from .views import ProductViewsets
#定义路由对象
router = DefaultRouter()
#注册路由
router.register('/json',ProductViewsets)


urlpatterns = [
    #指定渲染注册页面
    path('/register',TemplateView.as_view(template_name='supermarket/register.html')),
    #指定渲染登录页面
    path('',TemplateView.as_view(template_name='supermarket/login.html')),
    path('/login',TemplateView.as_view(template_name='supermarket/login.html')),
    #注册操作
    path('/do_reg',Reg.as_view()),
    #登录操作
    path('/do_login',Login.as_view()),
    #商品列表页
    path('/productlist',check_login(ProList.as_view())),
    #用户注销
    path('/logout',Logout.as_view()),
    #删除商品
    path('/prodel',ProDel.as_view()),
    #修改商品
    path('/proedit',ProEdit.as_view()),
    #添加购物车
    path('/addcart',AddCart.as_view()),
    #购物车列表
    path('/cartlist',CartList.as_view()),
    #清空购物车
    path('/clearcart',ClearCart.as_view()),
    #删除购物车商品
    path("/delcart",DelCart.as_view()),
    #修改购物车
    path("/editcart",EditCart.as_view()),
    #批量修改购物车
    path("/doeditcart",DoEditCart.as_view()),
    #批量删除
    path("/group_del",Group_Del.as_view()),
    #个人信息
    path("/userinfo",UserInfo.as_view()),
    #修改密码
    path("/password_update",Password_update.as_view()),
    # 验证码
    path("/captcha",test_captcha),

]

#将路由注入
urlpatterns += router.urls
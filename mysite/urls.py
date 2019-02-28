"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
#正则路由依赖于re_path模块,主路由文件可以包含子路由文件，使用include模块
from django.urls import path,re_path,include
#导入文件路由库
from django.views.static import serve
#导入配置文件的路径
from mysite.settings import UPLOAD_ROOT
#导入整个自定义模块 使用逗号来分隔调用
from . import test,d1,d2,d3,d4,d5,d6,d7
from mytest.views import mytest_index,IndexView
#导入子应用
from myapp.views import myapp_index
#导入子应用 导入整体
#from myapp import views


urlpatterns = [
    #定义图片超链接路由
    re_path('^upload/(?P<path>.*)$',serve,{'document_root':UPLOAD_ROOT}),
    path('admin/', admin.site.urls),
    path('tu',test.tu),
    path('kaoshi',include('kaoshi.urls')),
    path('mytest',include('mytest.urls')),
    #定义首页 首页留空 第二个参数 指定路由方法
    path('',d7.index),
    #包含网上超市的路由文件
    path('supermarket',include('supermarket.urls')),
    #直接包含子应用的路由文件
    path('myapp',include('myapp.urls')),
    #再定义一个路由
    path('test',d2.test),
    #定义一个重定向页面
    path('123',d1.re_url),
    #使用多个网址来指向同一个路由方法
    path('456',d1.re_url),
    re_path('^test123/(.*)$',test.test123),
    #定义存储cookie的路由
    path('save_cookie',d1.save_cookie),
    #定义获取cookie的路由
    path('get_cookie',d1.get_cookie),
    #定义删除cookie的路由
    path('del_cookie',d1.del_cookie),
    #定义一个正则路由，可以使用\d数字
    #常用元字符 .匹配所有 \d数字 \D非数字 \w 字母数字_
    #如果在正则路由内，使用（）分组，那么django会认为进行路由传参
    # re_path('^test-\d+-.*$',d1.test_re)
    re_path('^test-(\d+)-(.*)$',d1.test_re),
    re_path('^email-(\w{3}@qq\.com)-(\d+)-([A-Z]+)$',d2.test_email),
    #存储session
    path('save_session',d3.save_session),
    #取session
    path('get_session',d3.get_session),
    #删除session
    path('del_session',d3.del_session),
    #获取访问ip
    path('get_ip',d4.get_ip),
    #获取json接口
    path('json',d5.test_json),
    #指定注册页面
    path('register',d5.test_register),
    #定义用户详情
    path('user_info',d5.user_info),
    #详情页
    path('d6_info',d6.d6_info),
    #注销逻辑
    path('d6_logout',d6.d6_logout),
    #定义图片验证码
    path('captcha',d6.test_captcha),
    #定义路由传参json
    re_path('^d7_json/(.*)$',d7.d7_json)
]
#统一捕获异常404
#项目名.模块名.方法名
handler404 = 'mysite.d2.page_not_found'
handler500 = 'mysite.d4.page_not_error'

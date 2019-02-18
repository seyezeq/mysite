from django.http import HttpResponse,HttpResponseRedirect

#导入类视图模块
from django.views import View

#导入类视图模板模块
from django.views.generic import TemplateView

#导入通用类视图模块
from django.views.generic import ListView

#导入数据库类
from mysite.models import User

#导入方法视图模板
from django.shortcuts import render


#定义一个通同类视图
class MyList(ListView):
    #指定模板名称
    template_name = 'myapp/mytem.html'
    #指定变量名称
    context_object_name = 'user_list'
    #读取数据库
    #使用重写
    def get_queryset(self):
        user_list = User.objects.all()
        return user_list

#定义一个混合视图
class MyClassDef(View):

    #定义一个方法视图
    def get(self,request):
        return render(request,'d2_404.html')




#定义一个子应用的视图方法
def myapp_index(request):
    return HttpResponse('这里是一个子应用的视图方法')

#定义一个类视图，用来渲染模板文件
class MyTem(TemplateView):
    #指定模板名称
    template_name = 'myapp/mytem.html'


#定义类视图
class MyView(View):

    hello = '你好啊'
    
    def get(self,request):
        return HttpResponse(self.hello)
    
    def post(self,request):
        return HttpResponse('这里是post方法')

    def put(self,request):
        return HttpResponse('这里是put方法')

    def delete(self,request):
        return HttpResponse('这里是delete方法')

#定义继承类
class MySon(MyView):
    def get(self,request):
        return HttpResponse(MyView.hello)


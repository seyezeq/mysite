from django.shortcuts import render
from django.http import HttpResponse

from django.views import View
from django.views.generic import TemplateView,ListView
from mysite.models import User
from django.shortcuts import render

from django.contrib.auth.hashers import make_password, check_password


class mytest_index(View):
    def get(self,request):

        print(check_password("123456", make_password("123456")))



        request.session['list'] = [1,2,3]

        slist = request.session.get('list')

        ulist = User.objects.filter(id__in=[46,47,48])
        print(ulist)

        username = request.COOKIES.get('username','none')

        return render(request,'test.html',locals())

class SaveCookie(View):

    #cookies = request.COOKIES

    def get(self,request):
        #定义回应
        response = HttpResponse("存储成功")
        response.set_cookie("username",'admin',max_age=3600)
        #返回回应
        return response


class IndexView(ListView):  
    """
        首页视图函数，继承 ListView ，展示从数据库中获取的文章列表   
    """
    template_name = "d7_index.html"
    context_object_name = "user_list"

    def get_queryset(self):
        """
            重写 get_queryset 方法，取出发表的文章并转换文章格式
        """
        user_list = User.objects.all()
        return user_list


class MyView(View):

    greeting = "Good Day"

    def get(self, request):
        return HttpResponse(self.greeting)

    def post(self,request):
        return HttpResponse('这里是post')

    def put(self,request):
        return HttpResponse('这里是put')

    def delete(self,request):
        return HttpResponse('这里是delete')

    


class MySon(MyView):

    def get(self,request):
        return HttpResponse(MyView.greeting)

    #def post(self,request):


    

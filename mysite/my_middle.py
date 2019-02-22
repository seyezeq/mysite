#导入中间件库
from django.utils.deprecation import MiddlewareMixin
#定义中间件类
class MyMiddle(MiddlewareMixin):
    #定义请求之前的方法
    def process_request(self,request):
        request.session['str'] = 'welcome'
        print('在请求之前')

    #定义请求之后的方法
    def process_response(self,request,response):
        print('在请求之后')
        del request.session['str']
        return response
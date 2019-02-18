from django.utils.deprecation import MiddlewareMixin
class Middle1(MiddlewareMixin):
    def process_request(self,request):
        print("来了")     # 不用return Django内部自动帮我们传递
    def process_response(self, request,response):
        print('走了')
        return response
from supermarket.views import *

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
            ip = request.META.get('REMOTE_ADDR')
            #判断访问者在一秒内来了不止一次
            if ip == request.session.get("ip") and in_time < seconds:
                #抛出异常 ,使用第二个参数来指定异常
                return render(request,"supermarket/404.html")
            else:
                #来的时间点存储
                request.session['req_time'] = time.time()
                request.session['ip'] = request.META.get('REMOTE_ADDR')
                #让访问者继续访问
                ret = func(request)
                return ret
        return func_limit
    return rate_limit

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


#定义商品列表页
class ProList(View):
    #定义商品列表方法
    @method_decorator(limit(seconds=0.001))
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




#定义批量删除逻辑
class Group_Del(View):
    def post(self,request):
        ids = request.POST.get("ids")
        #使用eval方法来强转为list
        ids = eval('['+ids+"]")
        #删除操作
        Product.objects.filter(id__in=ids).delete()
        return HttpResponse("ok")
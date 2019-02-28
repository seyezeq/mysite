from supermarket.views import *

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

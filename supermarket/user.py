from supermarket.views import *

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
        code = request.POST.get("code")
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

#定义注销功能
class Logout(View):
    #定义注销方法
    def get(self,request):
        #建立response对象
        response = HttpResponseRedirect("/supermarket/login")
        #删除cookie
        response.delete_cookie("username")
        return response
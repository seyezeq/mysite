from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from mysite.models import User
def he(request):
    name = request.POST.get('name')
    res = User.objects.filter(username=name).count()
    if res > 0:
        return HttpResponse("注册失败")
    else:
        user = User(username=name)
        user.save()
        return HttpResponse("ok")
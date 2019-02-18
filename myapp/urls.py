#导包
from django.urls import path,re_path
from myapp.views import myapp_index,MyView,MySon,MyTem,MyList,MyClassDef
#导入类视图模板模块
from django.views.generic import TemplateView


#写路由配置列表
urlpatterns = [

    path('/myapp_index',myapp_index),
    #定义一个匹配类视图的路由,必须用as_view()方法来初始化类
    path('/myview',MyView.as_view(hello='你好我是动态传参')),
    path('/myson',MySon.as_view()),
    path('/mytem',MyTem.as_view()),
    path('/mytem_one',TemplateView.as_view(template_name='d2_404.html')),
    path('/mylist',MyList.as_view()),
    path('/myclassdef',MyClassDef.as_view()),

]
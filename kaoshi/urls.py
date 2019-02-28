from django.urls import path,re_path
from django.views.generic import TemplateView
from kaoshi.views import he
urlpatterns = [
    path("",TemplateView.as_view(template_name="kaoshi/login.html")),
    path("/do_he",he),

]
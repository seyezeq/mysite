from django.urls import path,re_path,include
 
from mytest.views import MyView,MySon,mytest_index,SaveCookie

from django.views.generic import TemplateView
 
 
urlpatterns = [
    path('',mytest_index.as_view()),
    path('/savecookie',SaveCookie.as_view()),
]

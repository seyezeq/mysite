#导包
#导入模板模块
from django import template

#注册过滤器对象
register = template.Library()

#自定义过滤器
#在django内部，通过装饰器的方式来注册自定义过滤器
@register.filter
def my_str(val):
    return '$' + str(val)


#定义过滤器用来计算购物车内商品数量
@register.filter
def supermarket_count(val,cart_list):
    #容器，存储遍历的个数
    test_dict = {}
    #遍历数组
    for key in cart_list:
        #通过key来计算元素个数
        test_dict[key] = test_dict.get(key,0) + 1
    return test_dict[val]



#定义一个双参数的过滤器
@register.filter
def my_str_two(val,p1):
    return val + p1


#定义一个多参数的过滤器
#注册过滤器的时候，需要注册simple_tag
@register.simple_tag
def my_str_many(val,p1,p2):
    return val + p1 + p2

#定义加前缀或者后缀
@register.simple_tag
def my_str_test(val,p1,p2):
    #判断前缀
    _front = ''
    if p1 == "男":
        _front ='Mr'
    else:
        _front = 'Miss'

    #判断后缀
    _back = ''
    if int(p2) == 100:
        _back = '满分'
    elif int(p2) < 80:
        _back = '不及格'
    else:
        _back = '及格'
    
    return _front + val + _back 


#定义一个取余数的过滤器
@register.filter
def get_line(val):
    return int(val) % 2
#定义一个上下文处理器
import datetime
def get_daytime(request):
    now  = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    my_hour = int(datetime.datetime.now().strftime('%H'))
    if my_hour >=1 and my_hour <= 7:
        now_str = "早上好"
    elif my_hour>7 and my_hour <= 11:
        now_str = "上午好"
    elif my_hour >11 and my_hour <=18:
        now_str = "下午好"
    else:
        now_str = "晚上好"
    #给模板传递所有的变量
    return locals()
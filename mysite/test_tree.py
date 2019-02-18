#导包
import turtle
#随机模块
import random
#导入一个模块的所有属性
from turtle import *

#建立对象
t = turtle.Turtle()
#定义画布
w = turtle.Screen()

#封装树的方法
def tree(branchLen,t):
    if branchLen > 3:
        if 8 <= branchLen <= 12:
            #画枝叶和花
            #randint 生成随机整数，参数代表区间
            if random.randint(0,2) == 0:
                #着色
                t.color('snow')
            else:
                t.color('lightcoral')
        elif branchLen < 8 :
            #树干连接
            if random.randint(0,1) == 0:
                #着色
                t.color('snow')
            else:
                t.color('lightcoral')
        else:
            #轮廓
            t.color('sienna')
            #换画笔尺寸
            t.pensize( branchLen / 10 )

        #进行绘制
        t.forward(branchLen)
        #定义坐标
        a = random.random() * 1.5
        #向右位移
        t.right(20*a)
        b = random.random() * 1.5
        #递归调用
        tree(branchLen-10*b,t)
        #向左位移
        t.left(40*a)
        #继续绘制
        tree(branchLen-10*b,t)
        #向右位移
        t.right(20*a)
        t.up()
        #收尾
        t.backward(branchLen)
        t.down()

if __name__ == "__main__":
    #绘制屏幕画布
    t = turtle.Turtle()
    #定义我的窗口
    myWin = turtle.Screen()
    getscreen().tracer(5,0)
    #设置屏幕尺寸
    turtle.screensize(bg='wheat')
    t.left(90)
    t.up()
    t.backward(150)
    t.down()
    #着色
    t.color('sienna')
    #调用树的方法
    tree(70,t)
    #保存屏幕
    myWin.exitonclick()
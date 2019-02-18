# -*- encoding: utf-8 -*-

import turtle
import random
from turtle import *
from time import sleep

# t = turtle.Turtle()
# w = turtle.Screen()


def tree(branchLen, t):
    t.hideturtle()
    if branchLen > 3:
        if 2 <= branchLen <= 5:
            if random.randint(0, 2) == 0:
                t.color('snow')
            else:
                t.color('lightcoral')
            t.pensize(branchLen / 3)
        elif branchLen < 2:
            if random.randint(0, 1) == 0:
                t.color('snow')
            else:
                t.color('lightcoral')
            t.pensize(branchLen / 2)
        else:
            t.color('sienna')
            t.pensize(branchLen / 10)

        t.forward(branchLen)

        r = random.random()
        print(r)
        a = 1.6 * r
        t.right(20*a)

        b = 1.6 * r
        tree(branchLen-10*b, t)
        t.left(40*a)

        tree(branchLen-10*b, t)
        t.right(20*a)

        t.up()
        t.backward(branchLen)
        t.down()


def petal(m, t):  # 树下花瓣
    for i in range(m):
        a = 200 - 400 * random.random()
        b = 10 - 20 * random.random()
        t.pensize(2)
        t.up()
        t.forward(b)
        t.left(90)
        t.forward(a)
        t.down()
        t.color("lightcoral")
        t.circle(1)
        t.up()
        t.backward(a)
        t.right(90)
        t.backward(b)


def write_text(t):
    sleep(1)
    t.color("sienna")
    t.hideturtle()
    str1 = '十年育树百年育人'
    l1 = len(str1)
    left = -200
    right = 200
    for i in range(0, l1):
        t.penup()
        t.goto(left, -10+i*(-40))
        if i > 3:
            t.goto(right, -10+(i-4)*(-40))
        sleep(0.2)
        t.write(str1[i], font=('微软雅黑', 21, 'bold'))

    str2 = '积云教育！桃李满天下！'
    l2 = len(str2)
    for i in range(0, l2):
        t.penup()
        t.goto(-200+(i*40), -260)
        t.write(str2[i], font=('微软雅黑', 21, 'bold'))
        sleep(0.2)


def main():
    t = turtle.Turtle()
    myWin = turtle.Screen()
    getscreen().tracer(5, 0)
    turtle.screensize(bg='wheat')
    turtle.hideturtle()
    t.left(90)
    t.up()
    t.backward(150)
    t.down()
    t.color('sienna')
    tree(64, t)
    petal(100, t)
    write_text(t)
    myWin.exitonclick()

main()
turtle.mainloop()
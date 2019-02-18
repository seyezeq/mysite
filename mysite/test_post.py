#导包
import requests
#发送请求，requests模块在post请求时，使用data参数来进行传参
result = requests.post("http://localhost:8000/test",data={'id':'5678'})
#解码
html = result.content.decode("utf-8")

print(html)
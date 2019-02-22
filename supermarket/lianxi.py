import requests
from lxml import etree
import re
from pymysql import connect
url = 'http://127.0.0.1:8000/supermarket/do_login'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
data = {'username':123,'password':123}
ses = requests.session()
ses.post(url,data=data)
res = ses.get('http://127.0.0.1:8000/supermarket/productlist')
he = res.text
ret = etree.HTML(he)
res = ret.xpath("//tbody")

for i in res:
    dict = {}
    dict["id"] = i.xpath("./tr/td[1]/text()")[0]
    dict["name"] = i.xpath("./tr/td[2]/text()")[0]
    dict['price']= i.xpath("./tr/td[3]/input/@value")[0]
#人库
    conn = connect(host="127.0.0.1",port=3306,user="root",password="mysql",database="mydjango",charset="utf8")
    cur = conn.cursor()
    cur.execute("insert into productlist_spider values(0,'"+dict["id"]+"','"+dict["name"]+"','"+dict['price']+"')")
    conn.commit()
    conn.close()
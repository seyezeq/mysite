import requests
import json
#设置cookie
cookies = {'username':'admin'}
result = requests.get('http://127.0.0.1:8000/supermarket/json',cookies=cookies)
res = result.content.decode("utf-8")
res = json.loads(res)
print(type(res))
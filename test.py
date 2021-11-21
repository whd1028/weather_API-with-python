import urllib.request
from bs4 import BeautifulSoup

url_car = 'http://openapi.seoul.go.kr:8088'
serviceKey_car = '58795171617a6d6638327a4c504e77'
query_str = f"{url_car}/{serviceKey_car}/xml/VolInfo/1/1000/A-08/20180101/05"  # 질문 완성
request = urllib.request.Request(query_str)
response = urllib.request.urlopen(request)
html = BeautifulSoup(response,'html.parser')
result = html.find('result')
print("err?")

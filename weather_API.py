# import urllib
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd


"""
요청변수(Request Parameter)

항목명(국문)	항목명(영문)	항목크기	항목구분	샘플데이터	항목설명
서비스키	    ServiceKey  	4	        필수	   -	        공공데이터포털에서 받은 인증키
페이지 번호	    pageNo	        4	        옵션	   1	        페이지번호 Default : 1
한페이지 결과수	numOfRows	    4	        옵션	   10	        한 페이지 결과 수 Default : 10
응답자료형식	dataType	    4	        옵션	   XML	        요청자료형식(XML/JSON) Default : XML
자료 코드	    dataCd      	4	        필수	   ASOS         자료 분류 코드(ASOS)
날짜 코드	    dateCd          3	        필수	   DAY or HR    날짜 분류 코드(DAY)
시작일	        startDt	        8	        필수	   20100101	    조회 기간 시작일(YYYYMMDD)
종료일      	endDt	        8	        필수	   20100601	    조회 기간 종료일(YYYYMMDD) (전일(D-1)까지 제공)
지점 번호	    stnIds	        3	        필수	   108	        종관기상관측 지점 번호 (활용가이드 하단 첨부 참조)
"""

urlParaInfo = pd.read_table('OpenAPI_Project\weather_Requesr_Parameter.txt', sep='\t+')
print(urlParaInfo[["항목명(국문)","항목명(영문)","항목구분"]])

urlResponseInfo = pd.read_table('OpenAPI_Project\weather_Response_Element.txt', sep='\t+')
print(urlResponseInfo[["항목명(국문)","항목명(영문)","항목구분"]])

file = open("OpenAPI_Project\LocationCode.txt",'r',encoding='utf-8')
LoCode_File = file.read()
LoCode_File.replace("\n\n",",").replace("\n","").replace(" ","").split(",")

code = []
location = []
for i, v in enumerate(LoCode_File):
    if i % 3 == 0:
        code.append(v)
    elif i % 3 == 1:
        location.append(v)
LocationCode = dict(zip(location,code))
print(f"LocationCode = {LocationCode}")
file.close()

url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
serviceKey = 'alWF7jEKCtEPNyg65f4jcsYeQJp2MZlPNTOd8SNy9GW8%2FqptIPRBcFjfkTpxWMMf%2BKU9awopinM6DhePTTLoYw%3D%3D'

def Collect(stnIds, startDt, endDt, dataCd="ASOS"):
    qeury_str = f"{url}?serviceKey={serviceKey}&dataCd={dataCd}&dateCd=DAY&startDt={startDt}&endDt={endDt}&stnIds={stnIds}"
    request = urllib.request.Request(qeury_str)
    response = urllib.request.urlopen(request)

    html = BeautifulSoup(response,'html.parser')
    items = html.find_all('item')
    for item in items:
        pass

    
# location_dic = {"서울" : 108, "인천" : 112, "태백" : 216, "세종" : 239, "대전" : 133, "부산" : 159}
# print(location_dic.keys())
# location_name =  "서울" # input("검색 지역 : ")
# stnIds = location_dic[location_name]
# startDt = 20190101 #input("시작날짜 : ")
# endDt = 20190601 #input("종료날짜 : ")
# Collect(stnIds, startDt, endDt)





# qeury_str = f"{url}?serviceKey={serviceKey}&pageNo=1&numOfRows=10&dataType=XML&dataCd=ASOS&dateCd=DAY&startDt=20100101&endDt=20100601&stnIds=108"
# # print(qeury_str)
# request = urllib.request.Request(qeury_str)
# response = urllib.request.urlopen(request)

# # print(response)
# html = BeautifulSoup(response,'html.parser')
# items = html.find_all('item')
# print(items[0])
# for item in items:
#     print(item.stnid.text)
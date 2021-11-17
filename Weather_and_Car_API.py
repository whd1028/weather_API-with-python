# OpenAPI를 이용한 프로젝트
# 날씨에 따른 교통량 (서울)

# import urllib
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd


"""
날씨 정보 API
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

url_weather_ParaInfo = pd.read_table('OpenAPI_Project\weather_Requesr_Parameter.txt', sep='\t+')
# print(url_weather_ParaInfo[["항목명(국문)","항목명(영문)","항목구분"]])
url_car_ResponseInfo = pd.read_table('OpenAPI_Project\weather_Response_Element.txt', sep='\t+')
# print(url_car_ResponseInfo[["항목명(국문)","항목명(영문)","항목구분"]])

# 지역별 기상관측소 코드 파일처리
# file = open("OpenAPI_Project\LocationCode.txt",'r',encoding='utf-8')
# LoCode_File = file.read()
# LoCode_File = LoCode_File.replace("\n\n",",")
# LoCode_File = LoCode_File.replace("\n","")
# LoCode_File = LoCode_File.replace(" ","")
# LoCode = LoCode_File.split(",")
# code = []
# location = []
# for i, v in enumerate(LoCode):
#     if i % 3 == 0:
#         code.append(v)
#     elif i % 3 == 1:
#         location.append(v)
# LocationCode = dict(zip(location,code))
# print(f"LocationCode = {LocationCode}")
# file.close()

"""
교통량 API
요청인자
변수명	    타입	        변수설명	    값설명
KEY	        String(필수)	인증키	        OpenAPI 에서 발급된 인증키
TYPE	    String(필수)	요청파일타입	xml파일 : xmlf, 엑셀파일 : xls, json파일 : json
SERVICE	    String(필수)	서비스명	    VolInfo
START_INDEX	INTEGER(필수)	요청시작위치	정수 입력 (페이징 시작번호 입니다 : 데이터 행 시작번호)
END_INDEX	INTEGER(필수)	요청종료위치	정수 입력 (페이징 끝번호 입니다 : 데이터 행 끝번호)
SPOT_NUM	STRING(필수)	지점번호	
YMD	        STRING(필수)	년월일      	YYYYMMDD
HH	        STRING(필수)	시간	        HH
"""

"""
교통지점 API
요청인자
변수명	    타입	        변수설명	    값설명
KEY	        String(필수)	인증키	        OpenAPI 에서 발급된 인증키
TYPE	    String(필수)	요청파일타입	xml파일 : xmlf, 엑셀파일 : xls, json파일 : json
SERVICE	    String(필수)	서비스명	    SpotInfo
START_INDEX	INTEGER(필수)	요청시작위치	정수 입력 (페이징 시작번호 입니다 : 데이터 행 시작번호)
END_INDEX	INTEGER(필수)	요청종료위치	정수 입력 (페이징 끝번호 입니다 : 데이터 행 끝번호)
"""


def CollectWeather(startDt, endDt, stnIds=108, dataCd="ASOS"):
    url_weather = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
    serviceKey_weather = 'alWF7jEKCtEPNyg65f4jcsYeQJp2MZlPNTOd8SNy9GW8%2FqptIPRBcFjfkTpxWMMf%2BKU9awopinM6DhePTTLoYw%3D%3D'
    query_str = f"{url_weather}?serviceKey={serviceKey_weather}&dataCd={dataCd}&dateCd=DAY&startDt={startDt}&endDt={endDt}&stnIds={stnIds}"
    request = urllib.request.Request(query_str)
    response = urllib.request.urlopen(request)

    html = BeautifulSoup(response,'html.parser')
    items = html.find_all('item')
    for item in items:
        pass

def CollectTraffic(START_INDEX,END_INDEX,YMD,HH):
    # 교통량 조회 형식 : {url}/{인증키}/{요청파일타입}/{서비스명}/{요청시작위치}/{요청종료위치}/{지점번호}/{년월일}/{시간}
    # 출력값 : SPOT_NUM : 지점번호,YMD : 년월일,HH:시간,IO_TYPE : 유입유출 구분,LANE_NUM : 차로번호,VOL : 교통량
    url_car = 'http://openapi.seoul.go.kr:8088'
    serviceKey_car = '58795171617a6d6638327a4c504e77'
    spot_dic = CollectSpot()
    spot_num_list = spot_dic.keys()
    for spot_num in spot_num_list:
        query_traffic = f"{url_car}/{serviceKey_car}/xml/SpotInfo/{START_INDEX}/{END_INDEX}/{spot_num}/{YMD}/{HH}"
        request = urllib.request.Request(query_traffic)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if rescode != 200:
            print("err : ",rescode)
            
        html = BeautifulSoup(response,'html.parser')
        rows = html.find_all('row')
        for row in rows:
            print(row)


def CollectSpot():
    # 지점 조회 형식 : {url}/{인증키}/{요청파일타입}/{서비스명}/{페이지시작}/{페이지종료}
    url_car = 'http://openapi.seoul.go.kr:8088'
    serviceKey_car = '58795171617a6d6638327a4c504e77'
    query_spot = f"{url_car}/{serviceKey_car}/xml/SpotInfo/0/500"

    request = urllib.request.Request(query_spot)
    response = urllib.request.urlopen(request)

    html = BeautifulSoup(response,'html.parser')
    rows = html.find_all('row')
    spot_dic = {}
    for row in rows:
        spot_dic[row.spot_num.text] = row.spot_nm.text
    # print(spot_dic.keys())
    return spot_dic

CollectTraffic(1,5,20100101,12)

# # print(response)
# html = BeautifulSoup(response,'html.parser')
# items = html.find_all('item')
# print(items[0])
# for item in items:
#     print(item.stnid.text)
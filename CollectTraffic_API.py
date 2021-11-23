# OpenAPI를 이용한 프로젝트
# 날씨에 따른 교통량 (2018년 서울도심)

# import urllib
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
from TrafficSql import TrafficSql
import time


def collectTraffic():  # API로 자료수집하려 했으나 시간이 오래 걸리는 관계로 엑셀파일로 대체함
    # 교통량 조회 형식 : {url}/{인증키}/{요청파일타입}/{서비스명}/{요청시작위치}/{요청종료위치}/{지점번호}/{년월일}/{시간}
    url_car = 'http://openapi.seoul.go.kr:8088'
    serviceKey_car = '58795171617a6d6638327a4c504e77'
    # spot_num_list = collectAllSpot()  # 서울시에서 관측하는 모든 도로 리스트
    spot_num_list = collectInerCity()  # 서울시에서 관측하는 도심의 도로리스트

    ymd = dt.datetime(2018,8,13)  # 자료 시작날짜
    end_ymd = dt.datetime(2019,1,1)  # 자료 끝날짜
    hour = dt.timedelta(hours=1)   # 자료 날짜(시간) 간격

    while ymd != end_ymd:
        ymd += hour
        ymd_str = ymd.strftime('%Y%m%d')
        hour_str = ymd.strftime('%H')
        for spot_num in spot_num_list:
            query_str = f"{url_car}/{serviceKey_car}/xml/VolInfo/1/1000/{spot_num}/{ymd_str}/{hour_str}"  # 질문 완성
            request = urllib.request.Request(query_str)
            response = urllib.request.urlopen(request)
            if response.getcode() != 200:
                print("err!!")
            
            html = BeautifulSoup(response,'html.parser')
            if html == None:
                print("err!!!")
            result = html.find('result')
            if result == None:
                result = html.find('RESULT')

            try:  # 원인을 알수 없는 오류 떄문에 ..... ==> 아마도 집에서는 무선인터넷연결이라서?..
                if result.code.text == 'INFO-000':  # 요청한 날짜의 자료가 존재하는 경우
                    rows = html.find_all('row')
                    for row in rows:
                        TrafficSql.insertData(row.spot_num.text, row.ymd.text, row.hh.text, row.io_type.text, row.lane_num.text, row.vol.text)
                    
                elif result.code.text == 'INFO-200': # 	해당하는 데이터가 없는 경우 # 자료가 없는 경우 
                    TrafficSql.insertData(spot_num,ymd_str,hour_str,None,None,None)

                else:
                    print(f'err_code : {result.code.text} /err_msg : {result.message.text}')  # err
            except:
                file = open('err_url.txt','w')
                file.write(str(dt.datetime.now()))
                file.write(query_str)
                TrafficSql.insertData(spot_num,ymd_str,hour_str,None,None,None)

        print(f"{ymd} finish")
        # time.sleep(2)  # 휴식 => {중간에 html값이 없는 경우가 나오는데 너무 빨라서 그런가?해서 주는 휴식}
                
def collectAllSpot():
    # 지점 조회 형식 : {url}/{인증키}/{요청파일타입}/{서비스명}/{페이지시작}/{페이지종료}
    url_car = 'http://openapi.seoul.go.kr:8088'
    serviceKey_car = '58795171617a6d6638327a4c504e77'
    query_str = f"{url_car}/{serviceKey_car}/xml/SpotInfo/1/500"
    request = urllib.request.Request(query_str)
    response = urllib.request.urlopen(request)

    html = BeautifulSoup(response,'html.parser')
    rows = html.find_all('row')
    spot_num_list = []
    for row in rows:
        # print(row.spot_num.text)
        # print(row.spot_nm.text)
        spot_num_list.append(row.spot_num.text)
    return spot_num_list

def collectInerCity():
     # 지점 조회 형식 : {url}/{인증키}/{요청파일타입}/{서비스명}/{페이지시작}/{페이지종료}
    url_car = 'http://openapi.seoul.go.kr:8088'
    serviceKey_car = '58795171617a6d6638327a4c504e77'
    query_str = f"{url_car}/{serviceKey_car}/xml/SpotInfo/1/500"
    request = urllib.request.Request(query_str)
    response = urllib.request.urlopen(request)

    html = BeautifulSoup(response,'html.parser')
    rows = html.find_all('row')
    spot_num_list = []
    for row in rows:
        # print(row.spot_num.text)
        # print(row.spot_nm.text)
        spot_num = row.spot_num.text
        if spot_num[0] == "A":  # 도심의 도로코드는 A로 시작한다.
            spot_num_list.append(spot_num)
        else:
            # continue
            break  # 자료가 사전순으로 나오기 때문에
    return spot_num_list


collectTraffic()


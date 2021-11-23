# OpenAPI를 이용한 프로젝트
# 날씨에 따른 교통량 (2018년 서울도심)

# import urllib
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
from WeatherSql import WeatherSql
import time


def collectWeather(startDt=20180101, endDt=20190101, stnIds=108, dataCd="ASOS"):
    # 날씨 조회 형식 : {url}?serviceKey={인증키}&{자료코드}={ASOS}&{날짜코드}={DAY}&{시작일}={20180101}&{종료일}={20190101}&{지점번호}={108(서울)}
    url_weather = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
    serviceKey_weather = 'alWF7jEKCtEPNyg65f4jcsYeQJp2MZlPNTOd8SNy9GW8%2FqptIPRBcFjfkTpxWMMf%2BKU9awopinM6DhePTTLoYw%3D%3D'
    query_str = f"{url_weather}?serviceKey={serviceKey_weather}&dataCd={dataCd}&dateCd=DAY&startDt={startDt}&endDt={endDt}&stnIds={stnIds}"
    request = urllib.request.Request(query_str)
    response = urllib.request.urlopen(request)
    if response.getcode() != 200:
                print("err!!")
                exit(0)

    html = BeautifulSoup(response,'html.parser')
    # print(html.get_text)
    returnauthmsg = html.find('returnauthmsg')
    if returnauthmsg:
        print(returnauthmsg.text)
        time.sleep(2)
        collectWeather()
        exit(0)
        
    totalCount = html.find('totalcount')
    totalCount = int(totalCount.text)
    print(f"totalcount = {totalCount}")
    numOfRows = 61
    for pageNo in range(1,int(totalCount/numOfRows)+1):
        query_str = \
        f"{url_weather}?serviceKey={serviceKey_weather}&numOfRows={numOfRows}&pageNo={pageNo}&dataCd={dataCd}&dateCd=DAY&startDt={startDt}&endDt={endDt}&stnIds={stnIds}"
        request = urllib.request.Request(query_str)
        response = urllib.request.urlopen(request)
        html = BeautifulSoup(response,'html.parser')
        items = html.find_all('item')
        for item in items:
            tm = item.tm.text
            print(tm)
            # 비가 안오는 날도 있으니 주의하자
            if item.sumrn == None:
                sumrn = None
            else:
                sumrn = item.sumrn.text
            # 눈이 안오는 날도 있으니 주의하자
            if item.ddmefs == None:
                ddmefs = None
            else:
                ddmefs = item.ddmefs.text
            # ddMes  일 최심적설(cm)
            if item.ddmes == None:
                ddmes = None
            else:
                ddmes = item.ddmes.text
            # sumfogdur  안개 계속 시간(hr)
            if item.sumfogdur == None:
                sumfogdur = None
            else:
                sumfogdur = item.sumfogdur.text

            # inserData
            if sumrn or ddmefs or ddmes or sumfogdur:
                WeatherSql.insertData(tm,sumrn,ddmefs,ddmes,sumfogdur)
        
# collectWeather()
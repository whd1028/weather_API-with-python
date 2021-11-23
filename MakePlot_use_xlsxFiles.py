from matplotlib import colors
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from SqlConn import SqlConn 
import datetime as dt

# traffic = pd.read_excel('OpenAPI_Project\\trafficIn2018.xlsx') # 2018자료를 취합한것은 읽는데 너무 오래걸린다.
# 한 행에 하루에 시간대별로 데이터가있다.(일자 지점 0시 1시 2시 ...)
traffic = pd.read_excel('OpenAPI_Project\\1월 서울시 교통량 조사자료.xlsx',sheet_name='2018년 1월')
query_weather = "select * from weather"
weather = pd.read_sql(query_weather,SqlConn.connection)
SqlConn.close()
# 기상청API에서 눈,비,안개가 있는 날만 받아왔다.

# 한 해동안 교통량과 비,눈이 온 날의 강수량,적설량을 그래프로 그려보자 => 음...찝찝한데...
def year_Traffic_Weather():
    fig, ax1 = plt.subplots() 
    ax2 = ax1.twinx()  # y축 2개 사용할 준비

    # 월별로 데이터 취합하기
    badcondition = weather[(weather["SUNRN"] != None) or (weather["DDMES"] != None)]  # 비or눈 온날


# 한 달동안 교통량과 비,눈이 온 날의 강수량,적설량을 그래프로 그려보자(12개)
def month_Traffic_Weather(month):
    ymd = dt.datetime(2018,month,1)  # 자료 시작날짜
    end_ymd = dt.datetime(2018,month+1,1)  # 자료 끝날짜
    day = dt.timedelta(1)  # 자료 날짜(시간) 간격
    traffic.set_index('일자') # 인덱스를 날짜로 설정하겠다. 자료접근이 편하도록
    # while ymd != end_ymd:
    ymd_str = ymd.strftime('%Y%m%d')  # traffic 날짜 형식
    traffic[]
    
    
    ymd += day

# 한 해동안 비,눈이 안 온 날의 평균 교통량과 온 날의 평균쿄통량을 수치화해서 비교하자



month_Traffic_Weather(1)




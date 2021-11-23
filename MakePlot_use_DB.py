from matplotlib import colors
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from SqlConn import SqlConn 
import datetime as dt

query_traffic = "select * from cartraffic"
traffic = pd.read_sql(query_traffic,SqlConn.connection)

query_weather = "select * from weather"
weather = pd.read_sql(query_weather,SqlConn.connection)
SqlConn.close()

# 한달동안 일별로 교통량 그리기 
# 전체 데이터에서 1월의 교통량 데이터 고르기
ymd = dt.datetime(2018,1,1)  # 자료 시작날짜
end_ymd = dt.datetime(2018,2,1)  # 자료 끝날짜
day = dt.timedelta(1)  # 자료 날짜(시간) 간격

# traffic_1 => 1월의 교통량 담을 리스트
date = []
traffic_1 = []

for _ in range(int((end_ymd-ymd).days)):
    ymd_str = ymd.strftime('%Y%m%d')
    traffic_1.append(traffic[traffic.YMD == ymd_str].VOL.sum())
    date.append(ymd.strftime('%d'))
    ymd = ymd + day

fig, ax1 = plt.subplots() # 
ax2 = ax1.twinx()  # y축 2개 사용할 준비 

# ax1.bar(date,traffic_1,color='c') # 교통량 그리기
ax1.plot(date,traffic_1,'ro-',label='traffic')
ax1.legend(loc='upper right')

ax1.set_ylabel('traffic(red)')

plt.xlabel('day')


# 한달동안 눈이나 비가 온 날을 점으로 표시
rain = weather[["TM","SUMRN"]] # 날짜,비 정보만 모으기
rain = rain[rain["TM"].str.startswith("2018-01-")] # 2018년 1월 자료 모으기
# rain = weather[weather.SUMRN.notnull()] 
rain["SUMRN"] = rain["SUMRN"].fillna('0.0') # 비가 안 온 날 값 처리
rain["SUMRN"] = rain["SUMRN"].astype(float)  # 문자->숫자로 변환

snow = weather[weather.DDMES != None]
snow = snow[["TM","DDMES"]]

# ax2.plot(rain["TM"].str[-2:].values,rain["SUMRN"].values,'bo')  
ax2.bar(rain["TM"].str[-2:].values,rain["SUMRN"].values,color='b') # 강수량 그리기
ax2.set_ylabel("rain[mm](blue)")


ax1.set_zorder(ax2.get_zorder() + 1)
ax1.patch.set_visible(False)

plt.title("traffic-rain (seoul,2018-01)")
plt.show()
